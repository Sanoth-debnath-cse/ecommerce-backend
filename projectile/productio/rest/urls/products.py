from django.urls import path
from productio.rest.views.products import (
    PublicProductsListView,
    PublicProductsDetailsView,
)

urlpatterns = [
    path(
        "/<slug:product_slug>",
        PublicProductsDetailsView.as_view(),
        name="public.products-details",
    ),
    path("", PublicProductsListView.as_view(), name="public.products-list"),
]
