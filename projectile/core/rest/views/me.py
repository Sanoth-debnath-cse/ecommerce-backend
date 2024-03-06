from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from core.rest.serializers.me import PublicMeSerializer

User = get_user_model()


class PublicMeView(RetrieveUpdateAPIView):
    serializer_class = PublicMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return User.objects.get(pk=self.request.user.pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
