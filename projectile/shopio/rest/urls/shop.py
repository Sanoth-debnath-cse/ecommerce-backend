from django.urls import path

from shopio.rest.views.shop import ShopView, ShopDetailsView, PublicShopView

urlpatterns = [
    path("/<uuid:shop_uid>", ShopDetailsView.as_view(), name="shop.details"),
    path("/public", PublicShopView.as_view(), name="shop.public.details"),
    path("/create", ShopView.as_view(), name="shop.create"),
]
