from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from productio.models import Product

from productio.rest.serializers.products import PublicProductsListSerializer


class PublicProductsListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicProductsListSerializer

    def get_queryset(self):
        return Product.objects.filter(is_published__isnull=False)


class PublicProductsDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicProductsListSerializer

    def get_object(self):
        product_slug = self.kwargs.get("product_slug")

        try:
            return Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
