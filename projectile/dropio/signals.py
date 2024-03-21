from django.db.models.signals import post_save
from django.dispatch import receiver

from dropio.models import Drop


@receiver(post_save, sender=Drop)
def create_active_drop_for_shop(sender, instance, created, **kwargs):
    if created:
        shop = instance.shop
        shop.active_drop = instance
        shop.save(update_fields=["active_drop"])
