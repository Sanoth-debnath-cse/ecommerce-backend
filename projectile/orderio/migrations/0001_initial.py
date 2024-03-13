# Generated by Django 5.0.3 on 2024-03-13 14:25

import dirtyfields.dirtyfields
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("productio", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                (
                    "total_price",
                    models.DecimalField(decimal_places=4, default=0, max_digits=8),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ORDER_PLACED", "Order Placed"),
                            ("PROCESSING", "Processing"),
                            ("ON_THE_WAY", "On the way"),
                            ("OUT_FOR_DELIVERY", "Out for delivery"),
                            ("DELIVERED", "Delivered"),
                        ],
                        default="PROCESSING",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name="OrderItems",
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
                ("quantity", models.PositiveIntegerField(blank=True, default=0)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orderio.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="productio.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                blank=True, through="orderio.OrderItems", to="productio.product"
            ),
        ),
    ]
