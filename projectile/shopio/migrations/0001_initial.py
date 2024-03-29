# Generated by Django 5.0.3 on 2024-03-13 14:25

import dirtyfields.dirtyfields
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("updated_at", models.DateTimeField(blank=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("terms_condition", models.TextField(blank=True)),
                ("privacy_policy", models.TextField(blank=True)),
                ("short_pitch", models.CharField(blank=True, max_length=500)),
                (
                    "contact_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("contact_website", models.URLField(blank=True, null=True)),
                ("other_website", models.URLField(blank=True, null=True)),
                (
                    "shipping_charges",
                    models.DecimalField(decimal_places=4, default=0, max_digits=8),
                ),
                ("owner", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name="Addresses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("updated_at", models.DateTimeField(blank=True)),
                ("address", models.CharField(max_length=500)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopio.shop",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
    ]
