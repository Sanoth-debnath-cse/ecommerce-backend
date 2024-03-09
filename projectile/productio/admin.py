from django.contrib import admin

from productio.models import Product, ProductStock, ProductStockConnector

admin.site.register(Product)
admin.site.register(ProductStock)
admin.site.register(ProductStockConnector)
