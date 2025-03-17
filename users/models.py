from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.constants import UserFields


class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, password: str, **extra_fields: dict):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields: dict):
        extra_fields.setdefault(UserFields.IS_STAFF.value, True)
        extra_fields.setdefault(UserFields.IS_SUPERUSER.value, True)
        return self.create_user(email, password, **extra_fields)


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
    objects = CustomUserManager()
