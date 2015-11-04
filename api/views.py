from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from serializers import UserSerializer, GroupSerializer, BracketSerializer, CompetitorSerializer, PositionSerializer
from django.shortcuts import render

import json

from models import Bracket, Competitor, Position

# Create your views here.


def bracket_view(request):
    return render(request, 'api/bracket_view.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BracketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows brackets to be created, viewed and edited.
    """
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer


class CompetitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows competitors to be created, viewed and edited.
    """
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer


class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bracket positions to be created, viewed and edited.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        json_obj = request.data
        num_positions = int(len(json_obj['Competitors']) * 2 - 1)
        new_competitors = []
        bracket = Bracket(title=json_obj['Title'])
        bracket.save()
        print(type(bracket.id))
        for value in json_obj['Competitors']:
            competitor = Competitor(title=value['name'])
            competitor.save()
            new_competitors.append(competitor)
        for new_competitor in new_competitors:
            position = Position(position=num_positions,
                                parent=int(num_positions/2),
                                bracket_id=bracket.id,
                                competitor_id=new_competitor.id)
            position.save()
            num_positions -= 1
        while num_positions > 0:
            position = Position(position=num_positions,
                                parent=int(num_positions/2),
                                bracket_id=bracket.id,
                                competitor_id=None)
            position.save()
            num_positions -= 1
        return Response({"message": "Got some data!",
                         "Bracket": bracket.id})
    return Response({"message": "Hello World!"})
