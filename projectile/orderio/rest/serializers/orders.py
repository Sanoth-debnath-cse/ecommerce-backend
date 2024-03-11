from django.contrib.auth import get_user_model

from rest_framework import serializers

from productio.models import Product, ProductStockConnector
from productio.rest.serializers.products import PublicProductsCartSerializer

from orderio.models import Order, OrderItems
from orderio.choices import OrderType

from mediaroomio.models import MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

User = get_user_model()


class PublicOrderProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    # secondary_image = serializers.SerializerMethodField()

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
            # "secondary_image",
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

    # def get_secondary_image(self, obj):
    #     secondary_obj = MediaRoomConnector.objects.filter(
    #         product=obj, type=MediaKindChoices.SECONDARY_PRODUCT_IMAGE
    #     ).first()
    #     if secondary_obj:
    #         return PublicMediaRoomSerializer(
    #             secondary_obj.media_room, context=self.context
    #         ).data
    #     return None


class PrivateOrderSerializer(serializers.ModelSerializer):
    items = PublicProductsCartSerializer(many=True, read_only=True)
    products = PublicOrderProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid",
            "created_at",
            "updated_at",
        ]
