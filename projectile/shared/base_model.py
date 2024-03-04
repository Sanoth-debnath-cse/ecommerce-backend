import uuid

from django.db import models
from django.utils import timezone

from dirtyfields import DirtyFieldsMixin


class BaseModel(models.Model, DirtyFieldsMixin):
    class Meta:
        abstract = True

    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
