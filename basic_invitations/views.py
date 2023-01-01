from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import CreateInvitationSerializer
from .models import Invitation
from .app_settings import app_settings

class SendInvitationView(APIView):
    """
    View to create and send an invitation
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
        Create and send an invitation
        """
        if(app_settings.INVITATION_LIMIT):
            if(Invitation.objects.filter(inviter=request.user).count()>=app_settings.INVITATION_LIMIT):
                raise PermissionDenied("Too much invitation sent")
        serializer = CreateInvitationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        invite = Invitation.create(serializer.validated_data['email'],request.user)
        invite.save()
        invite.send_invitation(request)
        return Response("Invitation sent to "+serializer.validated_data['email'])
