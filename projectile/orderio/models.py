from django.contrib.auth import get_user_model
from django.db import models

from productio.models import Product
from shared.base_model import BaseModel

from .choices import OrderType

User = get_user_model()


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="orderio.OrderItems", blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    status = models.CharField(
        max_length=50, choices=OrderType.choices, default=OrderType.PROCESSING
    )


class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, blank=True)
