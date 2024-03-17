# Generated by Django 5.0.3 on 2024-03-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderio", "0006_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitems",
            name="total_product_price",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
    ]
