from django.urls import path, include

urlpatterns = [
    path("/order", include("shopio.rest.urls.orders")),
    path("/categories", include("shopio.rest.urls.category")),
    path("/products", include("shopio.rest.urls.product")),
    path("", include("shopio.rest.urls.shop")),
]
