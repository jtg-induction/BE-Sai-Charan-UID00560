from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    # created_at = models.DateTimeField(auto_now_add=True)
    # last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
