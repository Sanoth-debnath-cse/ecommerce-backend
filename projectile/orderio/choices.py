from django.db import models


class OrderType(models.TextChoices):
    ORDER_PLACED = "ORDER_PLACED", "Order Placed"
    PROCESSING = "PROCESSING", "Processing"
    ON_THE_WAY = "ON_THE_WAY", "On the way"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for delivery"
    DELIVERED = "DELIVERED", "Delivered"
