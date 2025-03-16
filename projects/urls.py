from django.urls import path

from projects.views import ProjectMemberApiViewSet

urlpatterns = [
    path(
        "projects/<str:action>/<int:pk>/",
        ProjectMemberApiViewSet.as_view({"patch": "partial_update"}),
        name="project-member-update",
    )
]
