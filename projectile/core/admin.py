from django.contrib.auth import get_user_model
from django.contrib import admin

# Register your models here.
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["uid", "phone"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Other",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "image",
                    "uid",
                    "slug",
                )
            },
        ),
        (
            "User Permission",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    list_filter = ["is_superuser", "is_staff"]
    search_fields = ("phone", "email")
    readonly_fields = ("password", "uid", "slug")
    ordering = ("-created_at",)
