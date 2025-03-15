from django.db import models

from users.models import CustomUser


class Todo(models.Model):
    """
    Model representing a Todo
    """

    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
