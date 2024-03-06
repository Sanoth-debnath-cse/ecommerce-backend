from django.db import models

from autoslug import AutoSlugField

from shared.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)


class Product(BaseModel):
    name = models.CharField(max_length=500)
    short_pitch = models.CharField(max_length=1000, blank=True)
    slug = AutoSlugField(populate_from="name", unique=True, unique_with="name")
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    stock = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
