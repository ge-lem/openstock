from django.shortcuts import render
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from .models import Organization
from .serializers import OrganizationSerializer

User = get_user_model()

class OrganizationPermission(permissions.BasePermission):
    """
    Special permission for an organization
    User must be anthentificated
    GET, POST all user
    PUT, PATCH managers on the organization
    DELETE owner of the organization
    """
    def has_object_permission(self, request, view, obj):
        if obj.isIndividual and request.method not in permissions.SAFE_METHODS:
            return False
        if request.user.is_staff:
            return True
        isowner = False
        ismanager = False
        if isinstance(obj, Organization):
            isowner = request.user == obj.owner
            ismanager = isowner or request.user in obj.managers.all()
        return ((isowner and request.method == 'DELETE') or
                (ismanager and request.method in ['PUT','PATCH'])
                or request.method in permissions.SAFE_METHODS)

    def has_permission(self, request, view):
        return request.user.is_authenticated


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Endpoint for the organization
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (OrganizationPermission,)

    def get_queryset(self):
        orgas = Organization.objects.all()
        
        indiv = self.request.query_params.get('indiv', None)
        if indiv is not None:
            indiv = indiv == 'true'
            orgas = orgas.filter(isIndividual=indiv)
        
        userid = self.request.query_params.get('userid', None)
        if(userid is not None):
            try:
                user = User.objects.get(pk=userid);
                orgas = orgas.filter(Q(managers__in = [user])|Q(owner=user)).distinct()
            except User.DoesNotExist:
                orgas = orgas.none()

        return orgas

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError:
            raise ValidationError({'name': ['Ce nom est déjà utilisé']}, code='unique')
