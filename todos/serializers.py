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
