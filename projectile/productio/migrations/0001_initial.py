# Generated by Django 5.0.3 on 2024-03-13 14:25

import autoslug.fields
import dirtyfields.dirtyfields
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mediaroomio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name="ProductStock",
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
                ("size", models.CharField(blank=True, max_length=100)),
                (
                    "stock",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "unit_price_per_size",
                    models.DecimalField(decimal_places=3, default=0, max_digits=8),
                ),
                ("size_out_of_stock", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=500)),
                ("short_pitch", models.CharField(blank=True, max_length=1000)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique_with=("name",)
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=255)),
                (
                    "unit_price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=8),
                ),
                ("details", models.TextField(blank=True)),
                ("sizing", models.TextField(blank=True)),
                ("care", models.TextField(blank=True)),
                ("delivery_and_returns", models.TextField(blank=True)),
                ("is_published", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="productio.category",
                    ),
                ),
                (
                    "images",
                    models.ManyToManyField(
                        blank=True,
                        through="mediaroomio.MediaRoomConnector",
                        to="mediaroomio.mediaroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name="ProductStockConnector",
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
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="productio.product",
                    ),
                ),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="productio.productstock",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.ManyToManyField(
                blank=True,
                through="productio.ProductStockConnector",
                to="productio.productstock",
            ),
        ),
    ]