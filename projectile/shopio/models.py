from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from shared.base_model import BaseModel

User = get_user_model()


class Shop(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ManyToManyField(User)
    description = models.TextField(blank=True)
    terms_condition = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    short_pitch = models.CharField(max_length=500, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_website = models.URLField(null=True, blank=True)
    other_website = models.URLField(null=True, blank=True)


class Addresses(BaseModel):
    address = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
