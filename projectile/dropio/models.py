from django.contrib.auth import get_user_model

from django.db import models

from shared.base_model import BaseModel

User = get_user_model()


class Drop(BaseModel):
    drop_date = models.DateField(blank=True, null=True)
    drop_time = models.TimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    drop_start_date = models.DateField(blank=True, null=True)
    drop_end_time = models.TimeField(blank=True, null=True)
    shop = models.ForeignKey("shopio.Shop", on_delete=models.CASCADE)
    user = models.ManyToManyField(
        to=User, through="dropio.DropUserConnector", blank=True
    )


class DropUserConnector(BaseModel):
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drop_code = models.CharField(max_length=20, blank=True)
