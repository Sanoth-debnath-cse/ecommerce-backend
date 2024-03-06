from django.urls import path

from shopio.rest.views.product import PrivateProductListView, PrivateProductDetailsView

urlpatterns = [
    path(
        "/<uuid:product_uid>",
        PrivateProductDetailsView.as_view(),
        name="private-product-details",
    ),
    path("", PrivateProductListView.as_view(), name="private.product-list"),
]
