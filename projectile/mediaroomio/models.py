from django.contrib.auth import get_user_model
from django.db import models

from versatileimagefield.fields import VersatileImageField, PPOIField

from productio.models import Product

from shopio.models import Shop
from shared.base_model import BaseModel

from .choices import MediaKindChoices

User = get_user_model()


class MediaRoom(BaseModel):
    # image
    image = VersatileImageField(
        width_field="width",
        height_field="height",
        ppoi_field="ppoi",
        null=True,
        blank=True,
    )
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    ppoi = PPOIField()

    # General Information
    type = models.CharField(
        max_length=50, choices=MediaKindChoices.choices, null=True, blank=True
    )


class MediaRoomConnector(BaseModel):
    # Relationship Important
    media_room = models.ForeignKey(MediaRoom, on_delete=models.CASCADE)

    # General Information
    type = models.CharField(max_length=50, choices=MediaKindChoices.choices)

    # Relationship ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
