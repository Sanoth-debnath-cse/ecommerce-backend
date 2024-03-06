from rest_framework import serializers

from mediaroomio.models import MediaRoom


class PublicMediaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaRoom
        fields = ["uid", "created_at", "updated_at", "image", "type"]
        read_only_fields = fields
