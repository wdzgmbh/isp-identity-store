import uuid

from django.db import models


class PrimaryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Account(PrimaryModel):
    line_id = models.CharField(max_length=30)

    # If there is no limitation, this might be null.
    down_speed_mbit = models.PositiveIntegerField(null=True)
    up_speed_mbit = models.PositiveIntegerField(null=True)

