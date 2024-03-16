import stripe
from django.conf import settings

from django.shortcuts import render, redirect, reverse

# from django.urls import reverse
from django.views import generic
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from orderio.models import Order, OrderItems
from productio.models import Product
from productio.rest.serializers.products import PublicProductsCartSerializer
from shopio.models import Shop

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        host = self.request.get_host()

        product_data = request.data
        product_data = product_data.get("products", [])

        # shop data
        try:
            shop = Shop.objects.latest("created_at")
            shipping_charges = shop.shipping_charges
        except Shop.DoesNotExist:
            raise NotFound(detail="Shop not found")

        total_price = 0
        line_items = []
        if len(product_data) > 0:
            order = Order.objects.create(user=user)

            for product in product_data:
                try:
                    product_obj = Product.objects.get(uid=product.get("uid"))
                except Product.DoesNotExist:
                    continue
                OrderItems.objects.create(
                    order=order,
                    product=product_obj,
                    size=product.get("size", ""),
                    quantity=product.get("selected_stock", 0),
                )
                total_price += product.get("selected_stock", 0) * product_obj.unit_price

                checkout_item = {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product_obj.name,
                            "images": [product.get("primary_image", None)],
                        },
                        "unit_amount": int(product_obj.unit_price * 100),
                    },
                    "quantity": product.get("selected_stock", 0),
                }
                line_items.append(checkout_item)

            order.total_price = total_price
            order.save()

            try:
                checkout_session = stripe.checkout.Session.create(
                    shipping_address_collection={
                        # "allowed_countries": ["USA", "CA"],
                    },
                    shipping_options=[
                        {
                            "shipping_rate_data": {
                                "type": "fixed_amount",
                                "fixed_amount": {
                                    "amount": int(shipping_charges * 100),
                                    "currency": "usd",
                                },
                                "display_name": "Charge",
                            }
                        }
                    ],
                    payment_method_types=["card"],
                    line_items=line_items,
                    mode="payment",
                    success_url=f"http://{host}/payment/success",
                    cancel_url=f"http://{host}/payment/cancel",
                )
                return Response(checkout_session.url)
            except Exception as e:
                return Response({"error": str(e)}, status=500)


def payment_success(request):
    context = {"payment_success": "success"}
    return render(request, "success.html", context)


def payment_cancel(request):
    context = {"payment_cancel": "cancel"}
    return render(request, "cancel.html", context)
