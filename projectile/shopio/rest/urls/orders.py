from django.urls import path

from shopio.rest.views.orders import PrivateOrderListView, PrivateOrderDetailView

urlpatterns = [
    path(
        "/<uuid:order_uid>",
        PrivateOrderDetailView.as_view(),
        name="private.order-detail",
    ),
    path("", PrivateOrderListView.as_view(), name="private.order-list"),
]
