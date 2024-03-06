from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound

from shopio.models import Shop
from shopio.rest.serializers.shop import ShopSerializer

from shared.permission import IsShopOwner


class ShopView(CreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]


class ShopDetailsView(RetrieveUpdateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]

    def get_object(self):
        shop_uid = self.kwargs.get("shop_uid")
        try:
            return Shop.objects.get(uid=shop_uid)
        except Shop.DoesNotExist:
            raise NotFound("Shop not found")
