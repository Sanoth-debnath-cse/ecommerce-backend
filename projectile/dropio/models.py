from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModel

User = get_user_model()


class DropUser(BaseModel):
    drop_phone = PhoneNumberField()
    drop_code = models.CharField(max_length=20, blank=True)


class Drop(BaseModel):
    drop_date = models.DateField(blank=True, null=True)
    drop_time = models.TimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    drop_expire_date = models.DateField(blank=True, null=True)
    drop_expire_time = models.TimeField(blank=True, null=True)
    shop = models.ForeignKey("shopio.Shop", on_delete=models.CASCADE)
    user = models.ManyToManyField(
        to=User, through="dropio.DropUserConnector", blank=True
    )
    drop_user = models.ManyToManyField(
        to=DropUser, through="dropio.DropUserConnector", blank=True
    )
    is_drop_stop = models.BooleanField(default=False)
    drop_code = models.CharField(max_length=150, blank=True)


class DropUserConnector(BaseModel):
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    drop_user = models.ForeignKey(
        DropUser, on_delete=models.CASCADE, null=True, blank=True
    )
