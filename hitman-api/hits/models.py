from cuser.models import CUser
from django.db import models

from hitman.utils.model_mixins import TimeStampedModel


class HitStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class Hit(TimeStampedModel, models.Model):
    assigned_to = models.ForeignKey(
        CUser, on_delete=models.CASCADE, related_name="assigned_to"
    )
    target_name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(
        max_length=9, null=False, choices=HitStatus.choices, default=HitStatus.ASSIGNED
    )
    requester = models.ForeignKey(
        CUser, on_delete=models.CASCADE, related_name="requester"
    )

    class Meta:
        db_table = "hits"
