from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Bracket(models.Model):
    title = models.CharField(max_length=255)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Competitor(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Position(models.Model):
    bracket = models.ForeignKey(Bracket)
    competitor = models.ForeignKey(Competitor, blank=True, null=True)
    position = models.IntegerField()
    parent = models.CharField(max_length=255)


class Chat(models.Model):
    text = models.TextField()
    bracket = models.ForeignKey(Bracket)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
