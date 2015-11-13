from django.db import models
# from django.contrib.auth.models import User
from swampdragon.models import SelfPublishModel
from .serializers import ChatSerializer
# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=255)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)


class Competitor(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    # user = models.ForeignKey(User, blank=True, null=True)


class Position(models.Model):
    bracket = models.ForeignKey(Bracket)
    competitor = models.ForeignKey(Competitor, blank=True, null=True)
    position = models.IntegerField()
    parent = models.CharField(max_length=255)


class Chat(SelfPublishModel, models.Model):
    serializer_class = ChatSerializer
    text = models.CharField(max_length=255)
