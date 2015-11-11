from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=255)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)


class Competitor(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)


class Position(models.Model):
    bracket = models.ForeignKey(Bracket)
    competitor = models.ForeignKey(Competitor, blank=True, null=True)
    position = models.IntegerField()
    parent = models.CharField(max_length=255)
