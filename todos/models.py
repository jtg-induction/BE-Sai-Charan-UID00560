from django.db import models

from users.models import CustomUser
from utils.models import BaseModel


class Todo(BaseModel):
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_completed = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
