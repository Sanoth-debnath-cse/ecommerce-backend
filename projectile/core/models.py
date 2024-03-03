import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField, PPOIField
from dirtyfields import DirtyFieldsMixin

from .utils import get_slug_full_name


class BaseModel(models.Model, DirtyFieldsMixin):
    class Meta:
        abstract = True

    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = PhoneNumberField(unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=get_slug_full_name, editable=False, unique=True)

    # Image
    image = VersatileImageField(
        width_field="width",
        height_field="height",
        ppoi_field="ppoi",
        null=True,
        blank=True,
    )
    height = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    ppoi = PPOIField()

    # additional settings for User
    USERNAME_FIELD = "phone"

    def __str__(self):
        name = f"{self.first_name} {self.last_name}"
        return f"Name: {name}, phone: {self.phone}"
