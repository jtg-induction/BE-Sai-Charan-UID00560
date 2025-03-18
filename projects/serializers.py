from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from projects.models import Project
from users.serializers import CustomUserSerializerWithTodoStats


class ProjectSerializer(BaseModelSerializer):

    existing_member_count = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "name", "status", "existing_member_count", "max_members"]

    def get_status(self, obj):
        return obj.get_status_display()


class ProjectSerializerWithReport(BaseModelSerializer):
    report = CustomUserSerializerWithTodoStats(many=True, exclude_fields=["id"])

    class Meta:
        model = Project
        fields = ["name", "report"]
