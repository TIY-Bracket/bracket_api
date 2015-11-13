from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Bracket, Competitor, Position
from swampdragon.serializers.model_serializer import ModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        field = ('id', 'url', 'name')


class BracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracket
        fields = ('id', 'title', 'start_dt', 'end_dt')


class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ('id', 'title',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'position', 'parent', 'bracket', 'competitor')


class ChatSerializer(ModelSerializer):
    class Meta:
        model = 'bracket_api.Chat'
        publish_fields = ('text', )
        update_fields = ('text', )
