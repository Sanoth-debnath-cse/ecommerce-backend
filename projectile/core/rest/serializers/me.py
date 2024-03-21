from django.contrib.auth import get_user_model

from rest_framework import serializers

from shopio.models import Shop
from shopio.rest.serializers.shop import ShopDetailsSerializer

User = get_user_model()


class PublicMeSerializer(serializers.ModelSerializer):
    shop = serializers.SerializerMethodField()

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
            "is_staff",
            "is_superuser",
            "shop",
        ]
        read_only_fields = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
            "phone",
            "is_staff",
            "is_superuser",
        ]

    def get_shop(self, obj):
        if obj.is_staff and obj.is_superuser:
            shob_obj = Shop.objects.filter(owner=obj).first()
            if shob_obj:
                return ShopDetailsSerializer(shob_obj).data
            else:
                return None
        return None
