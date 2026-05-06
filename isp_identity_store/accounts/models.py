import datetime

import ipaddress

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

    @property
    def last_session(self):
        return self.session_set.order_by('-created_at').first()

    def __str__(self):
        if self.line_id:
            return self.line_id

        return super().__str__()

class Session(PrimaryModel):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )

    session_id = models.CharField(max_length=128, verbose_name="Session ID")

    circuit_id = models.CharField(max_length=128, verbose_name="Circuit ID")
    remote_id = models.CharField(max_length=128, verbose_name="Remote ID")

    # 123.123.123.123/32
    ip_address = models.CharField(max_length=18, verbose_name="IP Address")
    # 2001:0db8:0000:0000:0000:0000:0000:0001/128
    ipv6_prefix = models.CharField(max_length=43, verbose_name="IPv6 Prefix")
    ipv6_pd_prefix = models.CharField(max_length=43, verbose_name="IPv6 Prefix Delegation")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    last_seen_at = models.DateTimeField(auto_now_add=True, verbose_name="Last Seen")
    terminated_at = models.DateTimeField(blank=True, null=True, verbose_name="Stopped")

    @property
    def status(self):
        if self.terminated_at:
            return "Stopped"

        d = datetime.datetime.now(tz=datetime.timezone.utc) - self.last_seen_at

        if d.total_seconds() > 60 * 5:
            return "Timed Out"

        return "Started"

    def clean(self):
        _ = ipaddress.IPv4Network(self.ip_address)
        _ = ipaddress.IPv6Network(self.ipv6_prefix)
        _ = ipaddress.IPv6Network(self.ipv6_pd_prefix)

