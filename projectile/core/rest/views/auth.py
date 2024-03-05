from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from core.rest.serializers.auth import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
