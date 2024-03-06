from django.urls import path, include

urlpatterns = [path("", include("productio.rest.urls.products"))]
