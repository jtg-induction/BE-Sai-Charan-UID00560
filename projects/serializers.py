from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import serializers

from projects.models import Project, ProjectMember
from projects.settings import PROJECT_STATUS
from users.models import CustomUser
from users.serializers import CustomUserSerializerWithTodoStats
from utils.serializers import BaseModelSerializer


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


class ProjectUpdateMemberSerializer(serializers.ModelSerializer):

    user_ids = serializers.PrimaryKeyRelatedField(
        source="members", many=True, queryset=CustomUser.objects.all(), write_only=True
    )
    logs = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Project
        fields = ["user_ids", "logs"]

    def get_logs(self, instance):
        return self.context.get("logs", {})

    def get_users_to_add(self, instance, member_ids, project_current_members):
        user_project_data = list(
            CustomUser.objects.filter(id__in=member_ids).annotate(
                project_detail=ArrayAgg("projectmember__project_id")
            )
        )
        new_members = []
        logs = {}

        for member in user_project_data:
            if member in project_current_members:
                logs[member.id] = f"User is already a Member."
                continue
            if len(member.project_detail) >= 2:
                logs[member.id] = f"Cannot add as User is a member in two projects."
                continue
            if len(project_current_members) >= instance.max_members:
                logs[member.id] = (
                    f"Project cannot have more than {instance.max_members} members."
                )
                continue
            new_members.append(member)
            logs[member.id] = f"User added to project successfully."

        project_members_to_add = [
            ProjectMember(project=instance, member=member) for member in new_members
        ]
        ProjectMember.objects.bulk_create(project_members_to_add)

        return logs

    def get_users_to_remove(self, instance, members_data, project_current_members):
        remove_user = []
        logs = {}
        for member in members_data:
            if member in project_current_members:
                remove_user.append(member)
                logs[member.id] = "User removed successfully."
            else:
                logs[member.id] = "User is not a member of project."
        ProjectMember.objects.filter(project=instance, member__in=remove_user).delete()

        return logs

    def update(self, instance, validated_data):

        members_data = validated_data.pop("members", None)
        member_ids = [member.id for member in members_data] if members_data else []
        project_current_members = instance.members.all()
        logs = {}
        if "add" == self.context["action"]:
            logs = self.get_users_to_add(instance, member_ids, project_current_members)

        else:
            logs = self.get_users_to_remove(
                instance, members_data, project_current_members
            )

        self.context["logs"] = logs
        return instance
