from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound, ValidationError

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
                "This Phone number already used by another user"
            )
        except User.DoesNotExist:
            return phone

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long!"
            )
        return password

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
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
        refresh = RefreshToken.for_user(user)
        validated_data["refresh"], validated_data["access"] = str(refresh), str(
            refresh.access_token
        )

        return validated_data


class UserTokenSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(
        min_length=5,
        max_length=100,
        write_only=True,
    )
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone=phone)
            attrs["user"] = user
        except User.DoesNotExist:
            raise NotFound(detail="User does not exists")

        if not user.check_password(password):
            raise NotFound(detail="Invalid user password")

        return attrs

    def create(self, validated_data):
        user: User = validated_data.get("user")

        role = self.context.get("request").query_params.get("as", None)

        if role == "admin":
            if not (user.is_superuser and user.is_staff):
                raise ValidationError({"detail": "Only admin can perform this action"})
        refresh = RefreshToken.for_user(user)
        validated_data["refresh"], validated_data["access"] = str(refresh), str(
            refresh.access_token
        )
        return validated_data
