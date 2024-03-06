from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from productio.models import Product
from shopio.rest.serializers.product import (
    PrivateProductListSerializer,
    PrivateProductDetailsSerializer,
)

from shared.permission import IsShopOwner


class PrivateProductListView(ListCreateAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateProductListSerializer

    def get_queryset(self):
        return Product.objects.select_related("category").filter()


class PrivateProductDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateProductDetailsSerializer

    def get_object(self):
        product_uid = self.kwargs.get("product_uid")

        try:
            return Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            raise NotFound(detail="Product does not exists")
