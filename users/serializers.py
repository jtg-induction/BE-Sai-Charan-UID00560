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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "date_joined",
            "token",
        ]
        read_only_fields = ["date_joined", "token"]

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        return data
