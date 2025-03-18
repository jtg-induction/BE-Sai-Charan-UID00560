from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from commons.serializers import BaseModelSerializer
from users.constants import UserFields
from users.models import CustomUser


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


class UserRegistrationSerializer(CustomUserSerializerWithBasicInfo):
    """
    Serializer for validating data in user register Api.
    """

    first_name = serializers.RegexField(
        regex=r"^[a-zA-Z0-9]+$",
        error_messages={"invalid": "Only alphanumeric characters are allowed."},
    )
    last_name = serializers.RegexField(
        regex=r"^[a-zA-Z0-9]+$",
        error_messages={"invalid": "Only alphanumeric characters are allowed."},
    )
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    token = serializers.SerializerMethodField()

    class Meta(CustomUserSerializerWithBasicInfo.Meta):
        fields = CustomUserSerializerWithBasicInfo.Meta.fields + [
            UserFields.PASSWORD.value,
            "confirm_password",
            "token",
        ]
        read_only_fields = CustomUserSerializerWithBasicInfo.Meta.read_only_fields + [
            "token"
        ]

    def get_token(self, user):
        try:
            token, _ = Token.objects.get_or_create(user=user)
            return token.key
        except Exception:
            raise serializers.ValidationError({"token": "Unable to create a token"})

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match."}
            )
        return data

    def validate_password(self, password):
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return super().create(validated_data)
