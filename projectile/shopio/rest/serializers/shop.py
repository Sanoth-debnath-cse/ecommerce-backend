from rest_framework import serializers

from shopio.models import Shop


class ShopSerializer(serializers.ModelSerializer):
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


class PublicShopSerializer(ShopSerializer):
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
        ]
        read_only_fields = fields
