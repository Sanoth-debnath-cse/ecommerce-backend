from rest_framework import serializers


class PrivateDashboardSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField(read_only=True, default=0)
    total_order_placed = serializers.IntegerField(read_only=True, default=0)
    total_processing = serializers.IntegerField(read_only=True, default=0)
    total_on_way = serializers.IntegerField(read_only=True, default=0)
    total_out_for_delivery = serializers.IntegerField(read_only=True, default=0)
    total_delivered = serializers.IntegerField(read_only=True, default=0)
    total_products = serializers.IntegerField(read_only=True, default=0)
    total_published = serializers.IntegerField(read_only=True, default=0)
    total_unpublished = serializers.IntegerField(read_only=True, default=0)
    total_payment = serializers.DecimalField(
        max_digits=8, decimal_places=4, read_only=True, default=0
    )
    total_customer = serializers.IntegerField(read_only=True, default=0)
