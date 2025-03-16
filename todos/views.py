from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from todos.models import Todo
from todos.pagination import StandardResultsSetPagination
from todos.permissions import IsOwner
from todos.serializers import TodoViewSetCreateSerializer, TodoViewSetSerializer


class TodoAPIViewSet(ModelViewSet):
    """
    success response for create/update/get
    {
      "name": "",
      "done": true/false,
      "date_created": ""
    }

    success response for list
    [
      {
        "name": "",
        "done": true/false,
        "date_created": ""
      }
    ]
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TodoViewSetCreateSerializer

        return TodoViewSetSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-date_created")
