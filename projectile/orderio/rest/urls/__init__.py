from django.urls import path, include

urlpatterns = [path("", include("orderio.rest.urls.payments"))]
