import json

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from productio.models import Product, Category, ProductStock, ProductStockConnector

from mediaroomio.models import MediaRoom, MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

from shared.variables import versatile_image_size


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
    images = PublicMediaRoomSerializer(read_only=True, many=True)

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
            "stock_size",
            "images",
            "details",
            "sizing",
            "care",
            "delivery_and_returns",
            "is_published",
            "category",
            "primary_image",
            "secondary_image",
            "additional_images",
        ]
        read_only_fields = ["uid", "created_at", "updated_at", "is_published"]

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
    all_images = serializers.SerializerMethodField()

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
            "all_images",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]

    def get_all_images(self, instance):
        images = MediaRoom.objects.filter(mediaroomconnector__product=instance)
        return PublicMediaRoomSerializer(images, many=True, context=self.context).data
