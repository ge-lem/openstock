from djoser import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser import serializers, conf

User = get_user_model()

class UserSerializer(serializers.UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name', 'last_name',
        )
        read_only_fields = (settings.LOGIN_FIELD,)

class UserCreatePasswordRetypeSerializer(serializers.UserCreatePasswordRetypeSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "email",
            "password",
        )
        extra_kwargs = {'email': {'required': True,'allow_blank': False}}

