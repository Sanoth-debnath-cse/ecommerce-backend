from django.urls import path

from orderio.rest.views.payments import CreateCheckoutSessionView, my_webhook_view

urlpatterns = [
    path("/webhook/stripe", my_webhook_view, name="webhook-stripe"),
    path("", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
]
