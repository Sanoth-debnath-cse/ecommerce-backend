import json

from django.db.models import Sum

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from versatileimagefield.serializers import VersatileImageFieldSerializer

from productio.models import Product, Category, ProductStock, ProductStockConnector
from mediaroomio.models import MediaRoom, MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

from shared.variables import versatile_image_size


class PrivateImageCreateSerializer(serializers.Serializer):
    image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        sizes=versatile_image_size,
        write_only=True,
        required=False,
    )

    def create(self, validated_data):
        product_uid = self.context["view"].kwargs.get("product_uid")
        image = validated_data.pop("image", None)

        try:
            product = Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")

        if image:
            additional_image = MediaRoom.objects.create(
                image=image, type=MediaKindChoices.ADDITIONAL_PRODUCT_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=additional_image,
                type=MediaKindChoices.ADDITIONAL_PRODUCT_IMAGE,
                product=product,
            )
        return product


class PrivateProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "size",
            "stock",
        ]
        read_only_fields = fields


class PrivateProductListSerializer(serializers.ModelSerializer):
    stock = serializers.CharField(
        required=False, allow_blank=True, write_only=True, allow_null=True
    )
    stock_size = PrivateProductStockSerializer(
        read_only=True, many=True, source="stock"
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    primary_image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        sizes=versatile_image_size,
        write_only=True,
        required=False,
    )
    secondary_image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        sizes=versatile_image_size,
        write_only=True,
        required=False,
    )
    additional_images = serializers.ListField(
        child=VersatileImageFieldSerializer(
            sizes=versatile_image_size, write_only=True, allow_empty_file=True
        ),
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
    )
    primary_image_view = serializers.SerializerMethodField()
    is_stock = serializers.SerializerMethodField()
    total_sold_items = serializers.IntegerField(read_only=True, default=0)
    total_amount = serializers.IntegerField(read_only=True, default=0)
    # images = PublicMediaRoomSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
            "name",
            "short_pitch",
            "description",
            "unit_price",
            "stock",
            "stock_size",
            # "images",
            "details",
            "sizing",
            "care",
            "delivery_and_returns",
            "is_published",
            "category",
            "primary_image",
            "secondary_image",
            "additional_images",
            "primary_image_view",
            "is_stock",
            "total_sold_items",
            "total_amount",
        ]
        read_only_fields = ["uid", "created_at", "updated_at", "is_published"]

    def get_primary_image_view(self, obj):
        primary_obj = MediaRoomConnector.objects.filter(
            product=obj, type=MediaKindChoices.PRIMARY_PRODUCT_IMAGE
        ).first()
        if primary_obj:
            return PublicMediaRoomSerializer(
                primary_obj.media_room, context=self.context
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

    def create(self, validated_data):
        # extract all images fields
        primary_image = validated_data.pop("primary_image", None)
        secondary_image = validated_data.pop("secondary_image", None)
        additional_images = validated_data.pop("additional_images", [])

        # extract stock
        stock = validated_data.pop("stock", "")

        if isinstance(validated_data.get("category"), Category):
            validated_data["category"] = validated_data.get("category")

        product = Product.objects.create(**validated_data)

        if primary_image:
            main_image = MediaRoom.objects.create(
                image=primary_image, type=MediaKindChoices.PRIMARY_PRODUCT_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=main_image,
                type=MediaKindChoices.PRIMARY_PRODUCT_IMAGE,
                product=product,
            )
        if secondary_image:
            second_image = MediaRoom.objects.create(
                image=secondary_image, type=MediaKindChoices.SECONDARY_PRODUCT_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=second_image,
                type=MediaKindChoices.SECONDARY_PRODUCT_IMAGE,
                product=product,
            )

        for image in additional_images:
            side_image = MediaRoom.objects.create(
                image=image, type=MediaKindChoices.ADDITIONAL_PRODUCT_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=side_image,
                type=MediaKindChoices.ADDITIONAL_PRODUCT_IMAGE,
                product=product,
            )

        stock_data = json.loads(stock) if stock else []

        for data in stock_data:
            product_stock_data = ProductStock.objects.create(
                size=data.get("size"), stock=data.get("stock")
            )
            ProductStockConnector.objects.create(
                stock=product_stock_data, product=product
            )

        return product


# Product details serializer
class PrivateProductDetailsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    images = PublicMediaRoomSerializer(read_only=True, many=True)
    stock = PrivateProductStockSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "name",
            "short_pitch",
            "description",
            "unit_price",
            "stock",
            "is_published",
            "category",
            "images",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]
