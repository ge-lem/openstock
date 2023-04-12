from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.dispatch import receiver

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django_cas_ng.signals import cas_user_authenticated
from django_auth_ldap.backend import LDAPBackend
from django.conf import settings

from knox.views import LoginView as KnoxLoginView
from djoser.signals import user_registered

from basic_invitations.models import Invitation

from myauth.serializers import UserSerializer

User = get_user_model()


@receiver(user_registered)
def deactivate_invitation(sender, user, request, **kwargs):
    key = request.data['invitation_key']
    try:
        invite = Invitation.objects.get(key=key)
        invite.accepted = True
        invite.save()
    except BaseException:
        print("error accept invitation")
        pass


@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    user = LDAPBackend().populate_user(args.get('user').username)
    if user is not None:
        user.is_active = user.email.endswith(
            tuple(settings.LDAP_ACTIVE_EMAIL_FILTER))
        user.save()


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if (not request.user.is_authenticated):
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
        return super(LoginView, self).post(request, format=None)


class SelfView(APIView):
    """
    Endpoint to see personals informations/profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        instance = UserSerializer(request.user, context={'request': request})
        return Response(instance.data)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        users = User.objects.none()

        if ('ids' in self.request.query_params.keys()):
            ids_q = self.request.query_params.get('ids', None)
            ids = []
            if (ids_q is not None):
                try:
                    return User.objects.filter(
                        pk__in=[int(v) for v in ids_q.split(',')]).distinct()
                except ValueError:
                    users = users.none()

        search = self.request.query_params.get('search', None)
        if (search is not None):
            if (len(search) < 3):
                return User.objects.none()

            searchQ = (Q(username__icontains=search) |
                       Q(first_name__icontains=search) |
                       Q(last_name__icontains=search))
            users = User.objects.filter(searchQ).distinct()
        return users
