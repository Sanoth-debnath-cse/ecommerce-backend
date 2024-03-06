from django.db import models


class MediaKindChoices(models.TextChoices):
    MAIN_IMAGE = "MAIN_IMAGE", "Main Image"
    SIDE_IMAGE = "SIDE_IMAGE", "Side Image"
    PROFILE_IMAGE = "PROFILE_IMAGE", "Profile Image"
