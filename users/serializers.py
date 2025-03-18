from django.contrib.auth import get_user_model
from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from users.constants import UserFields


class CustomUserSerializer(BaseModelSerializer):
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


class CustomUserSerializerWithBasicInfo(CustomUserSerializer):
    """
    User Serializer for basic information of user
    """

    class Meta:
        model = get_user_model()
        fields = [
            UserFields.ID.value,
            UserFields.EMAIL.value,
            UserFields.FIRST_NAME.value,
            UserFields.LAST_NAME.value,
        ]
        read_only_fields = [UserFields.ID]


class CustomUserSerializerWithTodoStats(CustomUserSerializerWithBasicInfo):
    """
    User serializer with 'completed' and 'pending' task count under that user.
    """

    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta(CustomUserSerializerWithBasicInfo.Meta):
        fields = CustomUserSerializerWithBasicInfo.Meta.fields + [
            "pending_count",
            "completed_count",
        ]


class CustomUserWithProjectStats(CustomUserSerializerWithBasicInfo):
    """
    User serializer which includes count of projects of different status of which the user is part of.
    """

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())

    class Meta(CustomUserSerializerWithBasicInfo.Meta):
        fields = CustomUserSerializerWithBasicInfo.Meta.fields + [
            "to_do_projects",
            "in_progress_projects",
            "completed_projects",
        ]
        read_only_fields = CustomUserSerializerWithBasicInfo.Meta.read_only_fields + [
            "to_do_projects",
            "in_progress_projects",
            "completed_projects",
        ]
