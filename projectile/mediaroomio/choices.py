from django.db import models


class MediaKindChoices(models.TextChoices):
    PRIMARY_PRODUCT_IMAGE = "PRIMARY_PRODUCT_IMAGE", "Primary Product Image"
    SECONDARY_PRODUCT_IMAGE = "SECONDARY_PRODUCT_IMAGE", "Secondary Product Image"
    ADDITIONAL_PRODUCT_IMAGE = "ADDITIONAL_PRODUCT_IMAGE", "Additional Product Image"
    USER_PROFILE = "USER_PROFILE", "User Profile"
    USER_COVER = "USER_COVER", "User Cover"
    ADMIN_PROFILE = "ADMIN_PROFILE", "Admin Profile"
    ADMIN_COVER = "ADMIN_COVER", "Admin Cover"
    SHOP_PROFILE = "SHOP_PROFILE", "Shop Profile"
    SHOP_COVER = "SHOP_COVER", "Shop Cover"
