from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from todos.models import Todo
from todos.pagination import StandardResultsSetPagination
from todos.permissions import IsOwner
from todos.serializers import (
    TodoUpdateSerializer,
    TodoViewSetCreateSerializer,
    TodoViewSetSerializer,
)

todo_serializers = {
    "POST": TodoViewSetCreateSerializer,
    "PUT": TodoUpdateSerializer,
    "PATCH": TodoUpdateSerializer,
}


class TodoAPIViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD of Todos.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        return todo_serializers.get(self.request.method, TodoViewSetSerializer)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-date_created")
