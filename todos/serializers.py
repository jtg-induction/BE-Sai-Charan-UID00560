from django.contrib.auth import get_user_model
from rest_framework import serializers

from todos.models import Todo
from users.serializers import CustomUserSerializer


class TodoSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(exclude_fields=["id"])
    date_created = serializers.DateTimeField(format="%I:%M %p, %d %b, %Y")

    class Meta:
        model = Todo
        fields = ["id", "name", "done", "date_created", "user"]


class TodoSerializerWithUserName(serializers.ModelSerializer):
    creator = serializers.CharField()
    email = serializers.EmailField(source="user.email")
    date_created = serializers.DateTimeField(format="%I:%M %p, %d %b, %Y")

    class Meta:
        model = Todo
        fields = ["id", "name", "done", "date_created", "creator", "email"]


class TodoViewSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["name", "done", "date_created"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TodoViewSetSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source="id")
    todo = serializers.CharField(source="name")

    class Meta:
        model = Todo
        fields = ["todo_id", "todo", "done"]
