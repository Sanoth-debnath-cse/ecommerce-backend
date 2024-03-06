from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from core.rest.serializers.auth import UserRegistrationSerializer, UserTokenSerializer


class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserTokenSerializer
