from django.apps import AppConfig


class DropioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dropio"

    def ready(self):
        from . import signals
