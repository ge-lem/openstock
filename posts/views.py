import sys
from PIL import Image
from io import BytesIO
from datetime import timedelta

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import permissions
from rest_framework import viewsets, status, mixins
from rest_framework.parsers import (MultiPartParser,
                                    FormParser, JSONParser)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from taggit.models import Tag

from basic_organizations.models import Organization
from posts.models import Post, PhotoPost
from posts.serializers import PostSerializer, PostPublicSerializer

# Create your views here.


def compress_image(photo):
    # start compressing image
    if (photo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))):
        try:
            image_temporary = Image.open(photo)
            image_temporary.verify()

            image_temporary = Image.open(photo)
            output_io_stream = BytesIO()
            image_temporary.thumbnail((1250, 1250), Image.ANTIALIAS)
            rgba_image = image_temporary.convert('RGBA')
            background = Image.new("RGB", rgba_image.size, (255, 255, 255))
            background.paste(rgba_image, mask = rgba_image.split()[3])
            # saving output
            background.save(output_io_stream, format='JPEG', quality=75,
                                 optimize=True, progressive=True)
            output_io_stream.seek(0)
            photo = InMemoryUploadedFile(output_io_stream, 'ImageField',
                                         "%s.jpg" % photo.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(
                                             output_io_stream),
                                         None)
            return photo
        except BaseException as err:
            raise ValidationError("Wrong Image format", code=422)
    else:
        raise ValidationError("Wrong Image format", code=422)


class IsAdminOrIsOwner(permissions.BasePermission):
    """
    Permission checking if user is admin or if the object belongs
    to the current user.
    The object field must be 'user'
    """

    def has_object_permission(self, request, view, obj):
        ismanager = (
            request.user == obj.owner.owner) or (
            request.user in obj.owner.managers.all())
        return request.user.is_staff or ismanager


class IsOwnerOrOpen(permissions.BasePermission):
    """
    Permission checking if user is admin or if the object belongs
    to the current user.
    The object field must be 'user'
    """

    def has_object_permission(self, request, view, obj):
        ismanager = (
            request.user == obj.owner.owner) or (
            request.user in obj.owner.managers.all())
        return request.user.is_staff or ismanager or obj.status == Post.OPEN


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Endpoint for the post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    
    def get_queryset(self):
        posts = Post.objects.filter(Q(owner__managers__in=[self.request.user]) |
                                    Q(owner__owner=self.request.user))
        if (self.action == 'list'):
            search = self.request.query_params.get('search', None)
            tags = self.request.query_params.get('tags', None)
            status = self.request.query_params.get('status', None)
            orgaid = self.request.query_params.get('orga', None)
            order = self.request.query_params.get('order', 'e')

            if (order == "-c"):
                posts = posts.order_by('create_date')
            elif (order == "c"):
                posts = posts.order_by('-create_date')
            else:
                posts = posts.order_by('expire_date')

            if orgaid is not None:
                try:
                    orga = Organization.objects.get(pk=orgaid)
                    posts = posts.filter(owner=orga)
                except Organization.DoesNotExist:
                    posts = posts.none()

            if search is not None:
                searchQ = (Q(title__icontains=search) |
                           Q(description__icontains=search))
                posts = posts.filter(searchQ).distinct()
            if status is not None:
                posts = posts.filter(status=status)
            if tags is not None:
                posts = posts.filter(tags__name__in=tags.split(","))
        elif (self.action == 'retrieve'):
            posts = Post.objects.all()
        return posts

    def get_permissions(self):
        if self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrOpen]
        else:
            permission_classes = [IsAdminOrIsOwner, IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # When post closed set expire_date to now
        if (serializer.validated_data['status'] != instance.status and
                serializer.validated_data['status'] == Post.CLOSED):
            serializer.validated_data['expire_date'] = timezone.now().date()

        # When reopen post set expire_date to now + 30 days
        if (serializer.validated_data['status'] != instance.status and
                serializer.validated_data['status'] == Post.DRAFT and
                instance.status != Post.OPEN):
            serializer.validated_data['expire_date'] = timezone.now(
            ).date() + timedelta(days=30)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(update_user=self.request.user)

    @action(methods=['post'], detail=True)
    def update_thumbnail(self, request, pk=None):
        post = self.get_object()
        if post.thumbnail:
            post.thumbnail.delete()
        try:
            file = request.data['file']
            post.thumbnail = compress_image(file)
            post.save()
            return Response({'url': str(post.thumbnail)},
                            status=status.HTTP_200_OK)
        except KeyError:
            raise ParseError('Request has no resource file attached')
        except ValidationError as error:
            raise error

    @action(methods=['post'], detail=True)
    def add_photo(self, request, pk=None):
        post = self.get_object()
        try:
            file = request.data['file']
            photo = PhotoPost.objects.create(post=post,
                                             image=compress_image(file))
            photo.save()
            return Response({'url': str(photo.image)},
                            status=status.HTTP_200_OK)
        except KeyError:
            raise ParseError('Request has no resource file attached')
        except ValidationError as error:
            raise error

    @action(methods=['post'], detail=True)
    def delete_photo(self, request, pk=None):
        post = self.get_object()
        try:
            url = request.data['url']
            photo = PhotoPost.objects.get(post=post, image=url)
            if photo:
                photo.delete()
                return Response({"photo " + url + " deleted"},
                                status=status.HTTP_200_OK)
        except KeyError:
            raise ParseError('Request has no resource file attached')

    @action(methods=['get'], detail=False)
    def get_new(self, request):
        orgaid = self.request.query_params.get('orga', None)
        orga = None
        if orgaid is not None:
            try:
                orga = Organization.objects.filter(Q(managers__in=[self.request.user]) | Q(
                    owner=self.request.user)).get(pk=orgaid)
            except Organization.DoesNotExist:
                pass
        if orga is None:
            raise NotFound()

        post = None
        posts = Post.objects.filter(
            status=Post.DRAFT,
            owner=orga).order_by('-id')
        if (len(posts) != 0):
            post = posts[0]
        else:
            post = Post.objects.create(
                status=Post.DRAFT,
                owner=orga,
                title=settings.NEWPOST_TITLE,
                expire_date=timezone.now().date() + timedelta(days=settings.NEWPOST_LIFESPAN),
                update_user=request.user
            )
        return Response(PostSerializer(post).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def status(self, request):
        """
        Return the post status
        """
        return Response(dict((x, y) for x, y in Post.STATUS),
                        status=status.HTTP_200_OK)


class SearchPostViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    def get_serializer_class(self):
        
        if self.request.user.is_authenticated:
            return PostSerializer
        else:
            return PostPublicSerializer

            
    def get_permissions(self):
        if settings.PUBLIC_SEARCH and self.action in ['list', 'tags']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated,]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        posts = Post.objects
        search = self.request.query_params.get('search', None)
        tags = self.request.query_params.get('tags', None)
        orgaid = self.request.query_params.get('orga', None)
        order = self.request.query_params.get('order', 'e')
        typePost = self.request.query_params.get('type', 'b')

        if (order == "-c"):
            posts = posts.order_by('create_date')
        elif (order == "c"):
            posts = posts.order_by('-create_date')
        else:
            posts = posts.order_by('expire_date', '-create_date')

        if (typePost == "r"):
            posts = posts.filter(is_request=True)
        elif (typePost == "p"):
            posts = posts.filter(is_request=False)

        if orgaid is not None:
            try:
                orga = Organization.objects.get(pk=orgaid)
                posts = posts.filter(owner=orga)
            except Organization.DoesNotExist:
                posts = posts.none()

        if search is not None:
            searchQ = (Q(title__icontains=search) |
                       Q(description__icontains=search))
            posts = posts.filter(searchQ)
        if tags is not None:
            for t in tags.split(","):
                posts = posts.filter(tags__name__in=[t])

        visibilityCheck = lambda p: IsOwnerOrOpen().has_object_permission(self.request, self, p)
        return list(filter(visibilityCheck, posts.distinct()))

    @action(methods=['get'], detail=False)
    def tags(self, request):
        """
        Return list of all tags
        """
        return Response([x.name for x in Tag.objects.all()],
                        status=status.HTTP_200_OK)

class ImportPostsViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    nested = PostViewSet()
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    
    def get_serializer(self, *args, **kwargs):
        self.nested.request = self.request
        self.nested.format_kwarg = self.format_kwarg
        if (self.request.method == "POST" and
           isinstance(self.request.data, list) and
           not "many" in kwargs):
            return self.nested.get_serializer(many=True, *args, **kwargs)
        return self.nested.get_serializer(*args, **kwargs)
