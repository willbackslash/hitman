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

    def mark_as_completed(self):
        if not self.status == HitStatus.ASSIGNED:
            raise Exception(
                f"Could not mark as completed because hit has the status {self.status}"
            )

        self.status = HitStatus.COMPLETED
        self.save()

    def mark_as_failed(self):
        if not self.status == HitStatus.ASSIGNED:
            raise Exception(
                f"Could not mark as failed because hit has the status {self.status}"
            )

        self.status = HitStatus.FAILED
        self.save()

    class Meta:
        db_table = "hits"
