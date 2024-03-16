from django.urls import path, include

urlpatterns = [
    path("/checkout", include("orderio.rest.urls.payments")),
    path("", include("orderio.rest.urls.orders")),
]
