from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from .models import Post

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Serializer for Post objects.
    """
    photos = serializers.StringRelatedField(
        many=True,
        read_only=True,
     )
    thumbnail = serializers.StringRelatedField(
        read_only=True,
     )
    tags = TagListSerializerField()


    class Meta:
        model = Post
        fields = ['id', 'owner', 'status', 'tags', 'title',
                  'description', 'is_request', 'thumbnail', 'photos', 'create_date',
                  'expire_date', 'quantity', 'update_date', 'update_user']
        read_only_fields = ('create_date','update_date', 'update_user')
