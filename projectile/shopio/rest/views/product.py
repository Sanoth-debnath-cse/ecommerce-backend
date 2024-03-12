from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from productio.models import Product
from shopio.rest.serializers.product import (
    PrivateProductListSerializer,
    PrivateProductDetailsSerializer,
    PrivateImageCreateSerializer,
)
from mediaroomio.models import MediaRoom
from shared.permission import IsShopOwner


class PrivateProductListView(ListCreateAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateProductListSerializer

    def get_queryset(self):
        return (
            Product.objects.select_related("category").filter().order_by("-created_at")
        )


class PrivateProductDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateProductDetailsSerializer

    def get_object(self):
        product_uid = self.kwargs.get("product_uid")

        try:
            return Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            raise NotFound(detail="Product does not exists")


class PrivateImageCreateView(CreateAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateImageCreateSerializer


class PrivateProductPublishView(APIView):
    permission_classes = [IsShopOwner]

    def patch(self, request, *args, **kwargs):
        product_uid = self.kwargs.get("product_uid")

        try:
            product = Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            raise NotFound(detail="Product does not found")

        if product.is_published:
            product.is_published = False
        else:
            product.is_published = True

        product.save()

        return Response(status=status.HTTP_200_OK)


class PrivateImageDeleteView(APIView):
    permission_classes = [IsShopOwner]

    def delete(self, request, *args, **kwargs):
        image_uid = self.kwargs.get("image_uid")

        try:
            media_obj = MediaRoom.objects.get(uid=image_uid)
            media_obj.delete()
        except MediaRoom.DoesNotExist:
            raise NotFound(detail="Image not found")

        return Response(status=status.HTTP_200_OK)
