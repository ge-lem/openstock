from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer class of the Organization Model
    """
    class Meta:
        model = Organization
        fields = ('id', 'name', 'contact',
                  'description', 'owner', 'managers', 'isIndividual')
        read_only_fields = ('isIndividual', 'owner')

