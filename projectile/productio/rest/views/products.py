from django.db.models import Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from productio.models import Product, ProductStockConnector

from productio.rest.serializers.products import (
    PublicProductListSerializer,
    PublicProductsDetailsSerializer,
    PublicProductsCartSerializer,
)

from shopio.models import Shop

from mediaroomio.models import MediaRoomConnector
from mediaroomio.choices import MediaKindChoices


class PublicProductsListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(is_published__isnull=False)


class PublicProductsDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicProductsDetailsSerializer

    def get_object(self):
        product_slug = self.kwargs.get("product_slug")

        try:
            return Product.objects.get(slug=product_slug, is_published=True)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")


class PublicProductsCartVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PublicProductsCartSerializer(data=request.data, many=True)

        if serializer.is_valid():
            product_data = serializer.validated_data

            try:
                shop = Shop.objects.latest("created_at")
                shipping_charges = shop.shipping_charges
            except Shop.DoesNotExist:
                raise NotFound(detail="Shop not found")

            present_product_data = []
            list_product_data = []
            for data in product_data:
                list_product_data.append(dict(data))
            for product in list_product_data:
                slug = product.get("slug")
                selected_stock = product.get("quantity", 0)
                size = product.get("size", "")

                try:
                    get_product = Product.objects.get(slug=slug, is_published=True)

                    connector_obj = MediaRoomConnector.objects.filter(
                        product=get_product, type=MediaKindChoices.PRIMARY_PRODUCT_IMAGE
                    ).first()
                    path = None
                    if connector_obj:
                        primary_image = connector_obj.media_room.image
                        path = request.build_absolute_uri(primary_image.url)

                    # stock
                    present_stock = 0
                    stock_connector_obj = ProductStockConnector.objects.filter(
                        product=get_product, stock__size=size
                    ).aggregate(total_stock=Sum("stock__stock"))

                    stock = stock_connector_obj.get("total_stock")
                    if stock:
                        present_stock = stock
                    stock_difference = present_stock - selected_stock

                    is_available = True

                    if stock_difference < 0:
                        is_available = False

                    present_data = {
                        "uid": get_product.uid,
                        "slug": get_product.slug,
                        "created_at": get_product.created_at,
                        "updated_at": get_product.updated_at,
                        "name": get_product.name,
                        "unit_price": get_product.unit_price,
                        "selected_stock": selected_stock,
                        "present_stock": present_stock,
                        "stock_difference": stock_difference,
                        "is_available": is_available,
                        "size": size,
                        "primary_image": path,
                        "shipping_charges": shipping_charges,
                    }
                    present_product_data.append(present_data)
                except Product.DoesNotExist:
                    continue

            return Response(present_product_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
