from rest_framework import serializers
from .models import Invitation


class CreateInvitationSerializer(serializers.Serializer):
    """
    Serializer class of the Invitation Model
    """
    email = serializers.EmailField()

class InvitationSerializer(serializers.ModelSerializer):
    """
    Serializer class of the Invitation Model
    """
    created=serializers.DateTimeField(format="%d/%m/%y %H:%M")
    sent=serializers.DateTimeField(format="%d/%m/%y %H:%M")
    class Meta:
        model = Invitation
        fields = ('id', 'email','accepted', 'sent', 'created')
        read_only_fields = ('email','accepted', 'sent', 'created')

