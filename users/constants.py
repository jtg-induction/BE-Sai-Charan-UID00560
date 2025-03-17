from enum import Enum


class UserFields(Enum):
    """
    Fields within CustomUser model
    """

    ID = "id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    PASSWORD = "password"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    DATE_JOINED = "date_joined"
    LAST_LOGIN = "last_login"
    GROUPS = "groups"
    USER_PERMISSIONS = "user_permissions"
