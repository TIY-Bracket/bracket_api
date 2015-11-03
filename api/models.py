from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=255)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)


class Competitor(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class Positions(models.Model):
    bracket_id = models.ForeignKey(Bracket)
    competitor_id = models.ForeignKey(Competitor)
    position = models.IntegerField()
    parent = models.CharField(max_length=255)
