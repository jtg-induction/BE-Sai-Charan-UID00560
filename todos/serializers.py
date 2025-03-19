from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from todos.constants import TodoFields
from todos.models import Todo
from users.constants import UserFields
from users.serializers import CustomUserSerializerWithBasicInfo


class TodoSerializer(BaseModelSerializer):
    """
    Serializer for Todo model.
    """

    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = [
            TodoFields.ID.value,
            TodoFields.DATE_CREATED.value,
            TodoFields.DATE_COMPLETED.value,
            TodoFields.USER.value,
        ]


class TodoSerializerWithUserName(TodoSerializer):
    """
    TodoSerializer with special fields like 'user' etc.
    """

    user = CustomUserSerializerWithBasicInfo(exclude_fields=[UserFields.ID.value])
    creator = serializers.CharField()
    email = serializers.EmailField(source="user.email")
    date_created = serializers.DateTimeField(format="%I:%M %p, %d %b, %Y")

    class Meta(TodoSerializer.Meta):
        read_only_fields = TodoSerializer.Meta.read_only_fields + [
            "creator",
            "email",
        ]


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
