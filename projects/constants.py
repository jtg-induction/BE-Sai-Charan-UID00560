from enum import Enum

TO_BE_STARTED = 0
IN_PROGRESS = 1
COMPLETED = 2

PROJECT_STATUS = [
    (TO_BE_STARTED, "to-be-started"),
    (IN_PROGRESS, "in-progress"),
    (COMPLETED, "completed"),
]


class ProjectFields(Enum):
    """
    Fields within Project model.
    """

    ID = "id"
    NAME = "name"
    STATUS = "status"
    MAX_MEMBERS = "max_members"
    MEMBERS = "members"


class ProjectMemberFields(Enum):
    """
    Fields within ProjectMember model.
    """

    MEMBER = "member"
    PROJECT = "project"
