from django.db import models

from projects.constants import PROJECT_STATUS, TO_BE_STARTED, ProjectMemberFields
from users.models import CustomUser


class Project(models.Model):
    """
    Model that represents a project.
    """

    name = models.CharField(max_length=50, unique=True)
    status = models.PositiveIntegerField(choices=PROJECT_STATUS, default=TO_BE_STARTED)
    max_members = models.PositiveIntegerField()
    members = models.ManyToManyField(
        CustomUser, through="ProjectMember", related_name="projects"
    )

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Represents the association between a user and a project.

    This model is used as a through table for the many-to-many relationship
    between `Project` and `CustomUser`, allowing for additional customization
    if needed in the future.
    """

    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    ProjectMemberFields.MEMBER.value,
                    ProjectMemberFields.PROJECT.value,
                ],
                name="unique_enrollment",
            )
        ]
