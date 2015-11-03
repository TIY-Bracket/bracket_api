from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Bracket, Competitor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        field = ('url', 'name')


class BracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracket
        fields = ('title', 'start_dt', 'end_dt')


class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ('title',)
