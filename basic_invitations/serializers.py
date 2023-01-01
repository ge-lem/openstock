from rest_framework import serializers
from .models import Invitation


class CreateInvitationSerializer(serializers.Serializer):
    """
    Serializer class of the Invitation Model
    """
    email = serializers.EmailField()
