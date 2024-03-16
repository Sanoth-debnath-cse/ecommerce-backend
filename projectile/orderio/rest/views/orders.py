from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from orderio.models import Order, OrderItems
from orderio.rest.serializers.orders import (
    PublicOrderListSerializer,
    PublicOrderDetailSerializer,
)


class PublicOrderListView(ListAPIView):
    serializer_class = PublicOrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user=user).order_by("-created_at")


class PublicOrderDetailView(RetrieveAPIView):
    serializer_class = PublicOrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        order_uid = self.kwargs.get("order_uid")

        try:
            return Order.objects.get(user=user, uid=order_uid)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found")
