# Generated by Django 5.0.3 on 2024-03-21 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dropio", "0001_initial"),
        ("shopio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="active_drop",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="active_shop_drop",
                to="dropio.drop",
            ),
        ),
    ]
