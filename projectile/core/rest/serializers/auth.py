from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField
from versatileimagefield.serializers import VersatileImageFieldSerializer

from shared.variables import versatile_image_size

User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    phone = PhoneNumberField(required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        min_length=5,
        max_length=100,
        write_only=True,
    )
    image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        sizes=versatile_image_size,
        write_only=True,
        required=False,
    )
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate_phone(self, phone):
        try:
            User.objects.get(phone=phone)
            raise serializers.ValidationError(
                "This Phone number already by another user"
            )
        except User.DoesNotExist:
            return phone

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(
                {"details": "Password must be at least 6 characters long!"}
            )
        return password

    def create(self, validated_data):
        User.objects.get_or_create(
            phone=validated_data["phone"],
            defaults={
                "phone": validated_data.get("phone"),
                "password": make_password(validated_data.get("password")),
                "first_name": validated_data.get("first_name", ""),
                "last_name": validated_data.get("last_name", ""),
                "email": validated_data.get("email", ""),
                "image": validated_data.get("image", None),
            },
        )
