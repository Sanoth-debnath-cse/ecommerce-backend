# Generated by Django 5.0.3 on 2024-03-13 14:25

import autoslug.fields
import core.utils
import dirtyfields.dirtyfields
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
import versatileimagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
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
                ("first_name", models.CharField(blank=True, max_length=50)),
                ("last_name", models.CharField(blank=True, max_length=50)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        db_index=True, max_length=128, region=None, unique=True
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=core.utils.get_slug_full_name,
                        unique=True,
                    ),
                ),
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        height_field="height",
                        null=True,
                        upload_to="",
                        width_field="width",
                    ),
                ),
                ("height", models.PositiveIntegerField(blank=True, null=True)),
                ("width", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "ppoi",
                    versatileimagefield.fields.PPOIField(
                        default="0.5x0.5", editable=False, max_length=20
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
    ]
