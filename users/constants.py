from commons.constants import BaseModelFields


class UserFields(BaseModelFields):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    DATE_JOINED = "date_joined"
