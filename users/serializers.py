from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.constants import UserFields


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for interacting with users data.
    """

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = "__all__"
        read_only_fields = [
            UserFields.ID.value,
            UserFields.IS_STAFF,
            UserFields.IS_SUPERUSER,
            UserFields.DATE_JOINED.value,
            UserFields.LAST_LOGIN.value,
            UserFields.GROUPS.value,
            UserFields.USER_PERMISSIONS.value,
        ]
        extra_kwargs = {UserFields.PASSWORD.value: {"write_only": True}}
