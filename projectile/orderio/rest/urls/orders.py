from django.urls import path

from orderio.rest.views.orders import PublicOrderListView, PublicOrderDetailView

urlpatterns = [
    path(
        "/<uuid:order_uid>",
        PublicOrderDetailView.as_view(),
        name="public-order.details",
    ),
    path("", PublicOrderListView.as_view(), name="public-order.list"),
]
