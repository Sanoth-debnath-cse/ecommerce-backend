from rest_framework import serializers

from orderio.models import Order
from orderio.rest.serializers.orders import (
    PublicOrderListSerializer,
    PublicOrderDetailSerializer,
)


class PrivateOrderListSerializer(PublicOrderListSerializer):
    class Meta:
        model = Order
        fields = PublicOrderListSerializer.Meta.fields + ["is_ordered", "is_paid"]
        read_only_fields = fields.copy()
        read_only_fields.remove("status")


class PrivateOrderDetailSerializer(PublicOrderDetailSerializer):
    class Meta:
        model = Order
        fields = PublicOrderDetailSerializer.Meta.fields
        read_only_fields = fields.copy()
        read_only_fields.remove("status")
