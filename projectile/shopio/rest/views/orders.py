from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from orderio.models import Order
from shopio.rest.serializers.orders import (
    PrivateOrderListSerializer,
    PrivateOrderDetailSerializer,
)

from shared.permission import IsShopOwner


class PrivateOrderListView(ListAPIView):
    serializer_class = PrivateOrderListSerializer
    permission_classes = [IsShopOwner]

    def get_queryset(self):
        return (
            Order.objects.prefetch_related("orderitems_set")
            .filter()
            .order_by("-created_at")
        )


class PrivateOrderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateOrderDetailSerializer
    permission_classes = [IsShopOwner]

    def get_object(self):
        order_uid = self.kwargs.get("order_uid")

        try:
            return Order.objects.prefetch_related("orderitems_set").get(uid=order_uid)
        except Order.DoesNotExist:
            raise NotFound(detail="Oder does not exist")
