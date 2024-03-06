from rest_framework.generics import CreateAPIView

from shopio.rest.serializers.shop import ShopSerializer

from shared.permission import IsShopOwner


class ShopView(CreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
