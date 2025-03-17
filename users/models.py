from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.constants import UserFields


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A model representing a user.
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True)

    USERNAME_FIELD = UserFields.EMAIL.value
