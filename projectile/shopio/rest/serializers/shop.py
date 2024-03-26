from rest_framework import serializers

from dropio.models import Drop

from shopio.models import Shop


class ShopCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "uid",
            "created_at",
            "updated_at",
            "name",
            "description",
            "terms_condition",
            "privacy_policy",
            "short_pitch",
            "contact_number",
            "contact_email",
            "contact_website",
            "other_website",
            "shipping_charges",
        ]
        read_only_fields = [
            "uid",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        owner = self.context["request"].user

        shop = Shop.objects.create(**validated_data)
        shop.owner.add(owner)
        shop.save()
        return shop


class ShopDetailsSerializer(ShopCreateSerializer):
    drop_date = serializers.DateField(required=False, write_only=True, allow_null=True)
    drop_time = serializers.TimeField(required=False, write_only=True, allow_null=True)
    drop_expire_date = serializers.DateField(
        required=False, write_only=True, allow_null=True
    )
    drop_expire_time = serializers.TimeField(
        required=False, write_only=True, allow_null=True
    )
    drop_date_value = serializers.DateField(
        read_only=True, source="active_drop.drop_date"
    )
    drop_time_value = serializers.TimeField(
        read_only=True, source="active_drop.drop_time"
    )
    drop_expire_date_value = serializers.DateField(
        read_only=True, source="active_drop.drop_date"
    )
    drop_expire_time_value = serializers.TimeField(
        read_only=True, source="active_drop.drop_time"
    )

    class Meta:
        model = Shop
        fields = ShopCreateSerializer.Meta.fields + [
            "drop_date",
            "drop_time",
            "drop_expire_date",
            "drop_expire_time",
            "drop_date_value",
            "drop_time_value",
            "drop_expire_date_value",
            "drop_expire_time_value",
        ]
        read_only_fields = [
            "uid",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        drop_date = validated_data.pop("drop_date", None)
        drop_time = validated_data.pop("drop_time", None)
        drop_expire_date = validated_data.pop("drop_expire_date", None)
        drop_expire_time = validated_data.pop("drop_expire_time", None)

        instance = super().update(instance, validated_data)

        if drop_date and drop_time:
            Drop.objects.create(
                drop_date=drop_date,
                drop_time=drop_time,
                shop=instance,
                drop_expire_date=drop_expire_date,
                drop_expire_time=drop_expire_time,
            )

        return instance


class PublicShopSerializer(ShopDetailsSerializer):

    class Meta:
        model = Shop
        fields = ShopDetailsSerializer.Meta.fields
        read_only_fields = fields
