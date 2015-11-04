from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, BracketSerializer, CompetitorSerializer, PositionSerializer
from django.shortcuts import render

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

