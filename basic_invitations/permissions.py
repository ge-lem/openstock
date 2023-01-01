
from rest_framework import permissions
from .models import Invitation
from .app_settings import app_settings

class IsInvited(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if 'invitation_key' not in request.data:
            return False
        key = request.data['invitation_key']
        try:
            invite = Invitation.objects.get(key=key)
            if(invite.key_expired() or invite.accepted):
                return False
            if app_settings.INVITATION_ONESHOT:
                invite.accepted=True
                invite.save()
        except Invitation.DoesNotExist:
            return False
        return True

