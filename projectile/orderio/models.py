from django.contrib.auth import get_user_model
from django.db import models

from productio.models import Product
from shared.base_model import BaseModel

from .choices import OrderType

User = get_user_model()


class Order(BaseModel):
    order_id = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="orderio.OrderItems", blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    status = models.CharField(
        max_length=50, choices=OrderType.choices, default=OrderType.PROCESSING
    )
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=1000, blank=True)


class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, blank=True)
    size = models.CharField(max_length=100, blank=True)
