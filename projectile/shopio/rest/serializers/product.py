from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from productio.models import Product, Category

from mediaroomio.models import MediaRoom, MediaRoomConnector
from mediaroomio.choices import MediaKindChoices
from mediaroomio.rest.serializers.mediaroom import PublicMediaRoomSerializer

from shared.variables import versatile_image_size


class PrivateProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    product_image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        sizes=versatile_image_size,
        write_only=True,
        required=False,
    )
    images = serializers.ListField(
        child=VersatileImageFieldSerializer(
            sizes=versatile_image_size, write_only=True, allow_empty_file=True
        ),
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
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
            "product_image",
            "images",
            "all_images",
        ]
        read_only_fields = ["uid", "created_at", "updated_at", "is_published"]

    def get_all_images(self, instance):
        images = MediaRoom.objects.filter(mediaroomconnector__product=instance)
        return PublicMediaRoomSerializer(images, many=True, context=self.context).data

    def create(self, validated_data):
        # extract outside field
        product_image = validated_data.pop("product_image", None)
        images = validated_data.pop("images", [])

        if isinstance(validated_data.get("category"), Category):
            validated_data["category"] = validated_data.get("category")

        product = Product.objects.create(**validated_data)

        if product_image:
            main_image = MediaRoom.objects.create(
                image=product_image, type=MediaKindChoices.MAIN_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=main_image, type=MediaKindChoices.MAIN_IMAGE, product=product
            )

        for image in images:
            side_image = MediaRoom.objects.create(
                image=image, type=MediaKindChoices.SIDE_IMAGE
            )
            MediaRoomConnector.objects.create(
                media_room=side_image, type=MediaKindChoices.SIDE_IMAGE, product=product
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
