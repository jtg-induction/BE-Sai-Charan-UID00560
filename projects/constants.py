from commons.constants import BaseModelFields

TO_BE_STARTED = 0
IN_PROGRESS = 1
COMPLETED = 2

PROJECT_STATUS = {
    TO_BE_STARTED: "to-be-started",
    IN_PROGRESS: "in-progress",
    COMPLETED: "completed",
}


class ProjectFields(BaseModelFields):
    """
    Fields within Project model.
    """

    NAME = "name"
    STATUS = "status"
    MAX_MEMBERS = "max_members"
    MEMEBERS = "members"


class ProjectMemberFields(BaseModelFields):
    """
    Fields within ProjectMember model.
    """

    MEMBER = "member"
    PROJECT = "project"
