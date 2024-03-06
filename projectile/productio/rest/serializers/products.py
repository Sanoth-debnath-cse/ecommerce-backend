from rest_framework import serializers

from productio.models import Product

from shopio.rest.serializers.product import PrivateProductListSerializer


class PublicProductsListSerializer(PrivateProductListSerializer):
    class Meta:
        model = Product
        fields = PrivateProductListSerializer.Meta.fields + ["slug"]
        read_only_fields = PrivateProductListSerializer.Meta.fields + ["slug"]
