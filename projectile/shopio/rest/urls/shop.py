from django.urls import path

from shopio.rest.views.shop import ShopView

urlpatterns = [
    path("create", ShopView.as_view(), name="shop.create"),
]
