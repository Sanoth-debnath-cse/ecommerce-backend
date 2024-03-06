from rest_framework import serializers

from productio.models import Category


class PrivateCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uid", "created_at", "updated_at", "name"]
        read_only_fields = ["uid", "created_at", "updated_at"]
