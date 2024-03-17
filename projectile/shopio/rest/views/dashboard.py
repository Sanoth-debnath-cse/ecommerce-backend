from django.db.models import Sum, Count, Q
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from productio.models import Product
from shopio.rest.serializers.dashboard import PrivateDashboardSerializer

from shared.permission import IsShopOwner

from orderio.models import Order
from orderio.choices import OrderType


class PrivateDashboardView(RetrieveAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateDashboardSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        products = Product.objects.all()

        products_data = products.aggregate(
            total_products=Count("id", distinct=True),
            total_published=Count("id", distinct=True, filter=Q(is_published=True)),
            total_unpublished=Count("id", distinct=True, filter=Q(is_published=False)),
        )

        order_data = queryset.aggregate(
            total_orders=Count("id", distinct=True),
            total_order_placed=Count(
                "id", distinct=True, filter=Q(status=OrderType.ORDER_PLACED)
            ),
            total_processing=Count(
                "id", distinct=True, filter=Q(status=OrderType.PROCESSING)
            ),
            total_on_way=Count(
                "id", distinct=True, filter=Q(status=OrderType.ON_THE_WAY)
            ),
            total_out_for_delivery=Count(
                "id", distinct=True, filter=Q(status=OrderType.ON_THE_WAY)
            ),
            total_delivered=Count(
                "id", distinct=True, filter=Q(status=OrderType.DELIVERED)
            ),
            total_payment=Sum("total_price"),
            total_customer=Count("user", distinct=True),
        )

        order_data["total_products"] = products_data["total_products"]
        order_data["total_published"] = products_data["total_published"]
        order_data["total_unpublished"] = products_data["total_unpublished"]

        serializer = self.get_serializer(order_data)
        return Response(serializer.data)
