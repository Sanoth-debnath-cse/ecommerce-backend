# Generated by Django 5.0.3 on 2024-03-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dropio", "0004_alter_dropuser_drop_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="drop",
            name="is_drop_stop",
            field=models.BooleanField(default=False),
        ),
    ]