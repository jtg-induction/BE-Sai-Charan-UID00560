from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from projects.constants import ProjectFields
from projects.models import Project
from users.serializers import CustomUserSerializerWithTodoStats


class ProjectSerializer(BaseModelSerializer):
    """
    Serializer for Project model.
    """

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = [ProjectFields.ID.value]


class ProjectSerializerWithReport(ProjectSerializer):
    """
    Serilaizer for Project model which also includes specials fields.
    """

    status = serializers.SerializerMethodField()
    existing_member_count = serializers.IntegerField()
    report = CustomUserSerializerWithTodoStats(many=True, exclude_fields=["id"])

    class Meta(ProjectSerializer.Meta):
        read_only_fields = ProjectSerializer.Meta.read_only_fields + [
            "report",
            "existing_member_count",
        ]

    def get_status(self, obj):
        return obj.get_status_display()
