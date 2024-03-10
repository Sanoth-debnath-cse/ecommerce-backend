from django.urls import path
from productio.rest.views.products import PublicProductsCartVerifyView

urlpatterns = [
    path("", PublicProductsCartVerifyView.as_view(), name="public.products-cart-verify")
]
