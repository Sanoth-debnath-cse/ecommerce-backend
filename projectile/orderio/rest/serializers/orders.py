from django.contrib.auth import get_user_model

from rest_framework import serializers

from productio.models import Product
from orderio.models import Order, OrderItems

from mediaroomio.models import MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

User = get_user_model()


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "phone",
            "email",
        ]
        read_only_fields = fields


class PublicOrderProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()

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


class PublicOrderItemsListSerializer(serializers.ModelSerializer):
    product = PublicOrderProductListSerializer(read_only=True)

    class Meta:
        model = OrderItems
        fields = ["uid", "created_at", "updated_at", "product", "quantity", "size"]
        read_only_fields = fields


class PublicOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "order_id",
            "status",
            "address",
            "total_price",
            "user_cart_data",
            "order_shipping_charge",
        ]
        read_only_fields = fields


class PublicOrderDetailSerializer(PublicOrderListSerializer):
    user = PublicUserSerializer(read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = PublicOrderListSerializer.Meta.fields + [
            "user",
            "address",
            "order_shipping_charge",
            "user_cart_data",
            "products",
        ]
        read_only_fields = fields

    def get_products(self, obj):
        order_items = (
            obj.orderitems_set.all()
        )  # Assuming 'order items_set' is the related name
        return PublicOrderItemsListSerializer(
            order_items, context=self.context, many=True
        ).data
