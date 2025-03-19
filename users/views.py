from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserLoginSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
