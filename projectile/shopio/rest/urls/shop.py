from django.urls import path

from shopio.rest.views.shop import ShopView, ShopDetailsView

urlpatterns = [
    path("<uuid:shop_uid>", ShopDetailsView.as_view(), name="shop.details"),
    path("create", ShopView.as_view(), name="shop.create"),
]
