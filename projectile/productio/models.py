from django.db import models

from autoslug import AutoSlugField

from shared.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)


class Product(BaseModel):
    name = models.CharField(max_length=500)
    short_pitch = models.CharField(max_length=1000, blank=True)
    slug = AutoSlugField(populate_from="name", unique=True, unique_with="name")
    description = models.CharField(max_length=255, blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    stock = models.ManyToManyField(
        "productio.ProductStock", through="productio.ProductStockConnector", blank=True
    )
    images = models.ManyToManyField(
        "mediaroomio.MediaRoom", through="mediaroomio.MediaRoomConnector", blank=True
    )
    details = models.TextField(blank=True)
    sizing = models.TextField(blank=True)
    care = models.TextField(blank=True)
    delivery_and_returns = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )


class ProductStock(BaseModel):
    size = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=0, blank=True, null=True)
    unit_price_per_size = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    size_out_of_stock = models.BooleanField(default=False)


class ProductStockConnector(BaseModel):
    stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
