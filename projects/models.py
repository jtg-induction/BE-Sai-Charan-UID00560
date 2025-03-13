from django.db import models

from projects.settings import PROJECT_STATUS, TO_BE_STARTED
from users.models import CustomUser
from utils.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=50)
    status = models.IntegerField(choices=PROJECT_STATUS, default=TO_BE_STARTED)
    max_members = models.PositiveIntegerField()
    members = models.ManyToManyField(CustomUser, through="ProjectMember")

    def __str__(self):
        return self.name


class ProjectMember(BaseModel):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
