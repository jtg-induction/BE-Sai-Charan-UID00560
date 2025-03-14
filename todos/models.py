from __future__ import unicode_literals

from django.db import models


class Todo(models.Model):
    """
    Needed fields
    - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
    - name (max_length=1000)
    - done (boolean with default been false)
    - date_created (with default of creation time)
    - date_completed (set it when done is marked true)

    Add string representation for this model with todos name.
    """
