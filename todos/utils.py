from datetime import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Prefetch, Q, Value
from django.db.models.functions import Concat

from projects.models import Project
from projects.serializers import ProjectSerializer, ProjectSerializerWithReport
from todos.models import Todo
from todos.serializers import TodoSerializer, TodoSerializerWithUserName
from users.models import CustomUser
from users.serializers import (
    CustomUserSerializer,
    CustomUserSerializerWithTodoStats,
    CustomUserWithProjectStats,
)

# Add code to this util to return all users list in specified format.
# [ {
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com"
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_all_users():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of users data
    """

    users = CustomUser.objects.all()
    users_serializer = CustomUserSerializer(users, many=True)
    return users_serializer.data


# Add code to this util to  return all todos list (done/to do) along with user details in specified format.
# [{
#   "id": 1,
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Dec, 2021"
#   "creator" : {
#       "first_name": "Amal",
#       "last_name": "Raj",
#       "email": "amal.raj@joshtechnologygroup.com",
#   }
# },
# {
#   "id": 2,
#   "name": "Complete Python Assignment",
#   "status": "To Do",
#   "created_at": "5:30 PM, 13 Dec, 2021",
#   "creator" : {
#      "first_name": "Gurpreet",
#       "last_name": "Singh",
#       "email": "gurpreet.singh@joshtechnologygroup.com",
#   }
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_all_todo_list_with_user_details():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of todos
    """

    todos = Todo.objects.select_related("user").defer("user__id").all()
    todo_serializer = TodoSerializer(todos, many=True)
    return todo_serializer.data


# Add code to this util to return all projects with following details in specified format.
# [{
#   "id": 1,
#   "name": "Project A",
#   "status": "Done",
#   "existing_member_count": 4,
#   "max_members": 5
# },
# {
#   "id": 2,
#   "name": "Project C",
#   "status": "To Do",
#   "existing_member_count": 2,
#   "max_members": 4
# }]
# Note: use serializer for generating this format. use source for status in serializer field.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_projects_details():
    """
    Util to fetch all project details
    :return: list of dicts - List of project with details
    """

    projects = Project.objects.annotate(existing_member_count=Count("members")).all()
    project_serializer = ProjectSerializer(projects, many=True)
    return project_serializer.data


# Add code to this util to  return stats (done & to do count) of all users in specified format.
# [{
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "completed_count": 3,
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com",
#   "completed_count": 5,
#   "pending_count": 0
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_users_todo_stats():
    """
    Util to fetch todos list stats of all users on platform
    :return: list of dicts -  List of users with stats
    """

    users = CustomUser.objects.annotate(
        completed_count=Count("todo", filter=Q(todo__done=True)),
        pending_count=Count("todo", filter=Q(todo__done=False)),
    ).all()

    serializer = CustomUserSerializerWithTodoStats(users, many=True)
    return serializer.data


# Add code to this util to return top five users with maximum number of pending todos in specified format.
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 10
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_five_users_with_max_pending_todos():
    """
    Util to fetch top five user with maximum number of pending todos
    :return: list of dicts -  List of users
    """

    users = (
        CustomUser.objects.annotate(pending_count=Count("todo", Q(todo__done=False)))
        .order_by("-pending_count")
        .all()[:5]
    )
    serializer = CustomUserSerializerWithTodoStats(
        users, many=True, exclude_fields=["completed_count"]
    )
    return serializer.data


# Add code to this util to return users with given number of pending todos in specified format.
# e.g where n=4
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint : use annotation and aggregations
def fetch_users_with_n_pending_todos(n):
    """
    Util to fetch top five user with maximum number of pending todos
    :param n: integer - count of pending todos
    :return: list of dicts -  List of users
    """

    users = (
        CustomUser.objects.annotate(pending_count=Count("todo", Q(todo__done=False)))
        .filter(pending_count=n)
        .order_by("-pending_count")
        .all()[:5]
    )
    serializer = CustomUserSerializerWithTodoStats(
        users, many=True, exclude_fields=["completed_count"]
    )
    return serializer.data


# Add code to this util to return todos that were created in between given dates (add proper order too) and marked as
# done in specified format.
#  e.g. for given range - from 12-01-2021 to 12-02-2021
# [{
#   "id": 1,
#   "creator": "Amal Raj"
#   "email": "amal.raj@joshtechnologygroup.com"
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Jan, 2021"
# },
# {
#   "id": 2,
#   "creator": "Nikhil Khurana"
#   "email": "nikhil.khurana@joshtechnologygroup.com"
#   "name": "Complete Python Assignment",
#   "status": "Done",
#   "created_at": "5:30 PM, 02 Feb, 2021"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_completed_todos_with_in_date_range(start, end):
    """
    Util to fetch todos that were created in between given dates and marked as done.
    :param start: string - Start date e.g. (12-01-2021)
    :param end: string - End date e.g. (12-02-2021)
    :return: list of dicts - List of todos
    """
    start_date = datetime.strptime(start, "%d-%m-%Y")
    end_date = datetime.strptime(end, "%d-%m-%Y")

    todos = (
        Todo.objects.select_related("user")
        .annotate(creator=Concat("user__first_name", Value(" "), "user__last_name"))
        .filter(
            Q(date_created__date__gt=start_date)
            & Q(date_created__date__lt=end_date)
            & Q(done=True)
        )
    )

    serializer = TodoSerializerWithUserName(todos, many=True)
    return serializer.data


# Add code to this util to return list of projects having members who have name either starting with A or ending with A
# (case-insensitive) in specified format.
# [{
#   "project_name": "Project A"
#   "done": False
#   "max_members": 3
#   },
#   {
#   "project_name": "Project B"
#   "done": False
#   "max_members": 3
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_project_with_member_name_start_or_end_with_a():
    """
    Util to fetch project details having members who have name either starting with A or ending with A.
    :return: list of dicts - List of project data
    """

    projects = Project.objects.filter(
        Q(members__first_name__istartswith="A") | Q(members__last_name__iendswith="A")
    ).distinct()

    serializer = ProjectSerializer(projects, many=True, exclude_fields=["id"])
    return serializer.data


# Add code to this util to return project wise todos stats per user in specified format.
# [{
#   "project_title": "Project A"
#   "report": [
#       {
#           "first_name": "Amal",
#           "last_name": "Raj",
#           "email": "amal.raj@joshtechnologygroup.com",
#           "pending_count": 1,
#           "completed_count": 1,
#       },
#       {
#           "first_name": "Nikhil",
#           "last_name": "Khurana",
#           "email": "nikhil.khurana@joshtechnologygroup.com",
#           "pending_count": 0,
#           "completed_count": 5,
#       }
#   ]
# },
# {
#   "project_title": "Project B"
#   "report": [
#       {
#           "first_name": "Gurpreet",
#           "last_name": "Singh",
#           "email": "gurpreet.singh@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 15,
#       },
#       {
#           "first_name": "Naveen",
#           "last_name": "Kumar",
#           "email": "naveenk@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 5,
#       }
#   ]
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_project_wise_report():
    """
    Util to fetch project wise todos pending &  count per user.
    :return: list of dicts - List of report data
    """

    user_queryset = (
        CustomUser.objects.annotate(
            pending_count=Count("todo", filter=Q(todo__done=False)),
            completed_count=Count("todo", filter=Q(todo__done=True)),
        )
        .order_by("first_name")
        .only("id", "first_name", "last_name", "email")
    )

    # Prefetch members using the custom queryset
    projects = (
        Project.objects.prefetch_related(
            Prefetch("members", queryset=user_queryset, to_attr="report")
        )
        .order_by("name")
        .all()
    )

    serializer = ProjectSerializerWithReport(projects, many=True)
    return serializer.data


# Add code to this util to return all users project stats in specified format.
# [{
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project A", "Project C"],
#       "in_progress": ["Project B", "Project E"],
#       "completed": ["Project R", "Project L"],
#   }
# },
# {
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project C"],
#       "in_progress": ["Project B", "Project F"],
#       "completed": ["Project K", "Project L"],
#   }
# }]
# Note: Use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint: Use subquery/aggregation for project data.
def fetch_user_wise_project_done():
    """
    Util to fetch user wise project statuses.
    :return: list of dicts - List of user project data
    """

    users = (
        CustomUser.objects.annotate(
            to_do_projects=ArrayAgg(
                "projectmember__project__name",
                filter=Q(projectmember__project__status=0),
                distinct=True,
            ),
            in_progress_projects=ArrayAgg(
                "projectmember__project__name",
                filter=Q(projectmember__project__status=1),
                distinct=True,
            ),
            completed_projects=ArrayAgg(
                "projectmember__project__name",
                filter=Q(projectmember__project__status=2),
                distinct=True,
            ),
            total_projects=Count("projectmember__project"),
        )
        .order_by("-id")
        .all()
    )

    serializer = CustomUserWithProjectStats(users, many=True)
    return serializer.data
