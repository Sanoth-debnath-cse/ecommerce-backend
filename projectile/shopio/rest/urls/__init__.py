from django.urls import path, include

urlpatterns = [
    path("/", include("shopio.rest.urls.shop")),
]
