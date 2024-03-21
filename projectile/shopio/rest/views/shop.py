from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny

from shopio.models import Shop
from shopio.rest.serializers.shop import (
    ShopCreateSerializer,
    PublicShopSerializer,
    ShopDetailsSerializer,
)

from shared.permission import IsShopOwner


class ShopView(CreateAPIView):
    serializer_class = ShopCreateSerializer
    permission_classes = [IsShopOwner]


class ShopDetailsView(RetrieveUpdateAPIView):
    serializer_class = ShopDetailsSerializer
    permission_classes = [IsShopOwner]

    def get_object(self):
        shop_uid = self.kwargs.get("shop_uid")
        try:
            return Shop.objects.get(uid=shop_uid)
        except Shop.DoesNotExist:
            raise NotFound("Shop not found")


class PublicShopView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicShopSerializer

    def get_object(self):
        return Shop.objects.filter().first()
