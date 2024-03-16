from django.urls import path

from orderio.rest.views.payments import (
    CreateCheckoutSessionView,
    payment_success,
    payment_cancel,
)

urlpatterns = [
    path("/payment-cancel", payment_cancel, name="payment-cancel"),
    path("/payment-success", payment_success, name="payment-success"),
    path(
        "/checkout", CreateCheckoutSessionView.as_view(), name="create-checkout-session"
    ),
]
