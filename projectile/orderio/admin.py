from django.contrib import admin

from orderio.models import Order, OrderItems

admin.site.register(Order)
admin.site.register(OrderItems)
