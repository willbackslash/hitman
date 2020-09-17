from cuser.models import CUser
from django.db import models

from hitman.utils.model_mixins import TimeStampedModel


class ManagerUser(TimeStampedModel, models.Model):
    manager = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name="manager")
    user = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name="user")

    class Meta:
        db_table = "manager_users"
