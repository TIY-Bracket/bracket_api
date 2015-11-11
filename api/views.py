from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import UserSerializer, GroupSerializer, BracketSerializer, \
    CompetitorSerializer, PositionSerializer
from api.models import Bracket, Competitor, Position


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


def index(request):
    return render(request, 'api/index.html')


def bracket_view(request, bracket_id):
    bracket = Bracket.objects.get(pk=bracket_id)
    return render(request, 'api/bracket_view.html',
                  {"bracket_id": bracket_id,
                   "bracket": bracket},)


def bracket_create(request):
    return render(request, 'api/bracket_create.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


@api_view(['POST'])
def new_bracket(request):
    if request.method == 'POST':
        json_obj = request.data
        num_positions = int(len(json_obj['Competitors']) * 2 - 1)
        new_competitors = []
        bracket = Bracket(title=json_obj['Title'])
        bracket.save()
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
        return Response({"Bracket": bracket.id},
                        status=201)


@api_view()
def get_bracket(request, bracket_id):
    positions = Position.objects.filter(bracket_id=bracket_id)
    bracket_structure = []
    for position in positions:
        try:
            competitor = Competitor.objects.get(pk=position.competitor_id)
            bracket_structure.append({'name': competitor.title,
                                      'position': position.position,
                                      'parent': position.parent,
                                      'competitor': competitor.id,
                                      'position_id': position.id
                                      })
        except:
            bracket_structure.append({'name': '',
                                      'position': position.position,
                                      'parent': position.parent,
                                      'position_id': position.id
                                      })
    return Response(bracket_structure)


@api_view(['PUT'])
def update_bracket(request, bracket_id, competitor_id):
    current_player_record = Position.objects.filter(bracket_id=bracket_id,
                                                    competitor_id=competitor_id)
    Position.objects.filter(bracket_id=bracket_id,
                            position=current_player_record.values()[0]['parent']).update(competitor_id=competitor_id)

    return Response('hello')  # question for James. What should be returned?


@api_view(['PUT'])
def assign_competitor(request, competitor_id, user_id):
    competitor = Competitor.objects.get(pk=competitor_id)
    competitor.user_id = user_id
    competitor.save()

    return Response('hello')
