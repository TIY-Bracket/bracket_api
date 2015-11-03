from django.db import models


# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=100)
    start_dt = models.DateTimeFieldField(blank=True, null=True)
    end_dt = models.DateTimeFieldField(blank=True, null=True)
