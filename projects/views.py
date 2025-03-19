from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectUpdateMemberSerializer


class ProjectMemberApiViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    View Set for adding or removing users from a project.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectUpdateMemberSerializer

    def create(self, request, *args, **kwargs):
        """Handles adding members to the project."""

        project = self.get_object()
        serializer = self.get_serializer(
            instance=project,
            data=request.data,
            partial=True,
            context={"action": "add"},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"logs": serializer.data["logs"]},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """Handles removing members from the project."""

        project = self.get_object()
        serializer = self.get_serializer(
            instance=project,
            data=request.data,
            partial=True,
            context={"action": "remove"},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "logs": serializer.data["logs"],
            },
            status=status.HTTP_200_OK,
        )
