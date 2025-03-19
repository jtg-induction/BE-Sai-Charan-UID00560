from django.urls import path

from projects.views import ProjectMemberApiViewSet

urlpatterns = [
    path(
        "projects/<int:pk>/members/",
        ProjectMemberApiViewSet.as_view({"post": "create", "delete": "destroy"}),
        name="project-member-update",
    )
]
