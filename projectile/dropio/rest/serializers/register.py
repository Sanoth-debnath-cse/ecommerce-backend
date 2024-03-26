import random
from twilio.rest import Client
from django.conf import settings

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from shopio.models import Shop

from dropio.models import DropUser, DropUserConnector


class DropUserCreateSerializer(serializers.Serializer):
    drop_phone = PhoneNumberField(required=True)

    def create(self, validated_data):
        otp = random.randint(100000, 999999)

        drop_phone = validated_data.get("drop_phone", None)

        dropuser_obj = DropUser.objects.create(drop_phone=drop_phone, drop_code=otp)
        message = f"Your Drop Code is {otp}"
        client = Client(settings.TWILIO_MY_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        if drop_phone:
            drop_phone = str(drop_phone)
            client.messages.create(
                to=drop_phone, from_=settings.MY_TWILIO_NUMBER, body=message
            )

        # get shop
        shop_obj = Shop.objects.filter().first()
        if shop_obj:
            DropUserConnector.objects.create(
                drop=shop_obj.active_drop, drop_user=dropuser_obj
            )

        return validated_data
