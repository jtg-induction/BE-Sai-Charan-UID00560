from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from projects.constants import ProjectFields
from projects.models import Project
from users.serializers import CustomUserSerializerWithTodoStats


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = [ProjectFields.ID.value]


class ProjectSerializerWithReport(BaseModelSerializer):
    report = CustomUserSerializerWithTodoStats(many=True, exclude_fields=["id"])

    class Meta:
        model = Project
        fields = ["name", "report"]
