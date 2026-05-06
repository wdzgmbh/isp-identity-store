import uuid

from django.db import models
from django.urls import reverse


class PrimaryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Account(PrimaryModel):

    line_id = models.CharField(max_length=21, verbose_name="Line ID", unique=True)

    user = models.CharField(max_length=64, blank=True, null=True, verbose_name="PPPoE User", unique=True)
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name="PPPoE Password", help_text="Leave empty, if you do not want to change the password.")


    # If there is no limitation, this might be null.
    down_speed_mbit = models.PositiveIntegerField(null=True, verbose_name="Download Speed (in MBit/s)")
    up_speed_mbit = models.PositiveIntegerField(null=True, verbose_name="Upload Speed (in MBit/s)")

    def get_absolute_url(self):
        return reverse("accounts:detail-view", args=[str(self.id)])

    def clean(self):
        pass

    def __str__(self):
        if self.line_id:
            return self.line_id

        return super().__str__()