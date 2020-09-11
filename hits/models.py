from django.db import models
from cuser.models import CUser as User
from hitman.utils.model_mixins import TimeStampedModel


class Hit(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024)

    class Meta:
        db_table = "hits"
