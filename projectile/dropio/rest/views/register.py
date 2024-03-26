from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from dropio.rest.serializers.register import DropUserCreateSerializer


class DropUserCreateView(CreateAPIView):
    serializer_class = DropUserCreateSerializer
    permission_classes = [AllowAny]
