from django.db.models import Sum

from rest_framework import serializers

from mediaroomio.models import MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

from productio.models import Product, ProductStockConnector

from shopio.rest.serializers.product import PrivateProductListSerializer


class PublicProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    secondary_image = serializers.SerializerMethodField()
    is_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
            "name",
            "unit_price",
            "primary_image",
            "secondary_image",
            "is_stock",
        ]

    def get_primary_image(self, obj):
        primary_obj = MediaRoomConnector.objects.filter(
            product=obj, type=MediaKindChoices.PRIMARY_PRODUCT_IMAGE
        ).first()
        if primary_obj:
            return PublicMediaRoomSerializer(
                primary_obj.media_room, context=self.context
            ).data
        return None

    def get_secondary_image(self, obj):
        secondary_obj = MediaRoomConnector.objects.filter(
            product=obj, type=MediaKindChoices.SECONDARY_PRODUCT_IMAGE
        ).first()
        if secondary_obj:
            return PublicMediaRoomSerializer(
                secondary_obj.media_room, context=self.context
            ).data
        return None

    def get_is_stock(self, obj):
        stock_obj = (
            ProductStockConnector.objects.filter(product=obj).aggregate(
                total_stock=Sum("stock__stock")
            ),
        )
        stock = stock_obj[0].get("total_stock")
        if stock:
            return True
        return False


class PublicProductsDetailsSerializer(PrivateProductListSerializer):
    images = PublicMediaRoomSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = PrivateProductListSerializer.Meta.fields + ["images"]
        read_only_fields = PrivateProductListSerializer.Meta.fields + ["images"]


class PublicProductsCartSerializer(serializers.Serializer):
    slug = serializers.CharField()
    quantity = serializers.IntegerField()
    size = serializers.CharField()
