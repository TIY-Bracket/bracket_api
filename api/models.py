from django.db import models


# Create your models here.


class Bracket(models.Model):
    bracket_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_dt = models.DateField(blank=True, null=True)
    end_dt = models.DateField(blank=True, null=True)
