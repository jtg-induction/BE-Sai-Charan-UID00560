from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from utils.serializers import BaseModelSerializer


class CustomUserSerializer(BaseModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email"]


class CustomUserSerializerWithTodoStats(BaseModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "completed_count",
            "pending_count",
        ]


class CustomUserWithProjectStats(BaseModelSerializer):

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "to_do_projects",
            "in_progress_projects",
            "completed_projects",
        ]
