from django.urls import path

from shopio.rest.views.product import (
    PrivateProductListView,
    PrivateProductDetailsView,
    PrivateImageCreateView,
    PrivateProductPublishView,
    PrivateImageDeleteView,
)

urlpatterns = [
    path(
        "/<uuid:product_uid>/publish",
        PrivateProductPublishView.as_view(),
        name="private-product-publish",
    ),
    path(
        "/<uuid:product_uid>/add-image",
        PrivateImageCreateView.as_view(),
        name="private-product-image-create",
    ),
    path(
        "/<uuid:product_uid>",
        PrivateProductDetailsView.as_view(),
        name="private-product-details",
    ),
    path(
        "/image/<uuid:image_uid>",
        PrivateImageDeleteView.as_view(),
        name="private-product-image-delete",
    ),
    path("", PrivateProductListView.as_view(), name="private.product-list"),
]
