from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count
from rest_framework import serializers

from commons.serializers import BaseModelSerializer
from projects.constants import ProjectFields
from projects.models import Project, ProjectMember
from users.models import CustomUser
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


class ProjectSerializerWithReport(BaseModelSerializer):
    """
    Serializer that displays additional 'report' field.
    """

    report = CustomUserSerializerWithTodoStats(many=True, exclude_fields=["id"])

    class Meta:
        model = Project
        fields = ["name", "report"]


class ProjectUpdateMemberSerializer(serializers.ModelSerializer):
    """
    Serializer that handles adding and removing users from a project.
    """

    user_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    logs = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Project
        fields = ["user_ids", "logs"]

    def get_logs(self, instance):
        return self.context.get("logs", {})

    def get_users_to_add(self, instance, member_ids, project_current_members):
        user_project_data = CustomUser.objects.filter(id__in=member_ids).annotate(
            project_count=Count("projectmember__project_id")
        )

        new_members = []
        logs = {}

        for member in user_project_data:
            if len(project_current_members) >= instance.max_members:
                logs[member.id] = (
                    f"Project cannot have more than {instance.max_members} members."
                )
                continue
            if member.id in project_current_members:
                logs[member.id] = f"User is already a Member."
                continue
            if member.project_count >= 2:
                logs[member.id] = f"Cannot add as User is a member in two projects."
                continue
            new_members.append(member)
            logs[member.id] = f"User added to project successfully."

        project_members_to_add = [
            ProjectMember(project=instance, member=member) for member in new_members
        ]
        ProjectMember.objects.bulk_create(project_members_to_add)

        # Informing about non-existent users
        for member_id in member_ids:
            if member_id not in logs:
                logs[member_id] = "User doesn't exist."

        return logs

    def get_users_to_remove(self, instance, member_ids, project_current_members):
        remove_user = []
        logs = {}
        for member in member_ids:
            if member in project_current_members:
                remove_user.append(member)
                logs[member.id] = "User removed successfully."
            else:
                logs[member.id] = "User is not a member of project."
        ProjectMember.objects.filter(
            project=instance, member_id__in=remove_user
        ).delete()

        return logs

    def update(self, instance, validated_data):

        member_ids = validated_data.pop("user_ids", None)
        project_current_members = instance.members.values_list("id", flat=True)
        logs = {}
        if self.context["action"] == "add":
            logs = self.get_users_to_add(instance, member_ids, project_current_members)

        else:
            logs = self.get_users_to_remove(
                instance, member_ids, project_current_members
            )

        self.context["logs"] = logs
        return instance
