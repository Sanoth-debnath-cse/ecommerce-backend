# Generated by Django 4.2.7 on 2024-03-08 18:48

import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("mediaroomio", "0002_alter_mediaroom_type_alter_mediaroomconnector_type"),
        ("productio", "0002_alter_product_unit_price"),
    ]

    operations = [
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
        migrations.AddField(
            model_name="product",
            name="care",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="product",
            name="delivery_and_returns",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="product",
            name="details",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True,
                through="mediaroomio.MediaRoomConnector",
                to="mediaroomio.mediaroom",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="sizing",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.RemoveField(
            model_name="product",
            name="stock",
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