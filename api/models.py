from django.db import models


# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=255)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)
