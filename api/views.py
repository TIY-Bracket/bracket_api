from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import UserSerializer, GroupSerializer, BracketSerializer, \
    CompetitorSerializer, PositionSerializer
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout as auth_logout
#from django.contrib.auth.decorators import login_required
from django.conf import settings
from api.models import Bracket, Competitor, Position

# Create your views here.

#
#

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
    print(bracket_id)
    bracket = Bracket.objects.get(pk=bracket_id)
    return render(request, 'api/bracket_view.html',
                  {"bracket_id": bracket_id,
                   "bracket": bracket,},)



def bracket_create(request):
    print("THis is me!!!!!!!".center(100, '-'))
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


import requests
from django.http import HttpResponseRedirect
def send_email(email_address, subject, text):
    MAILGUN_KEY = settings.MAILGUN_KEY

    results = requests.post(
        "https://api.mailgun.net/v3/sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org/messages",
        auth=("api", MAILGUN_KEY),
        data={"from": "Bracket Guys <mailgun@sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org>",
              # need a valid email
              "to": email_address,
              "subject": subject,
              "text": text})

    print(results)
    print(results.text)
    return HttpResponseRedirect("/contacts")
    # return Response('hello')


# def send_notification(request):
#     username = request.data['username']
#     user = User.objects.filter(username=username)
#     if len(user) == 0:
#         return HttpResponse('That username is not in the database. ')
#
#
#     recipient = user[0].email
#     key = 'key-''
#     sandbox = 'sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org'
#     request_url = 'https://api.mailgun.net/v3/{}/messages'.format(sandbox)
#     request = requests.post(request_url, auth=('api', key), data={
#         'from': 'Mailgun Sandbox <postmaster@sandbox014f80db3f0b441e94e5a6faff21f392.mailgun.org>',
#         'to': recipient,
#         'subject': 'versus.live notification',
#         'text': 'You go head to head in 5 mins'
#     })


def contact(request):
    return render(request, 'api/contact.html')


def matchup(request, bracket_id, parent_id):
    competitors = Position.objects.filter(bracket_id=bracket_id, parent=parent_id)
    competitor_a = competitors[0]
    competitor_b = competitors[1]

    try:
        competitor = Competitor.objects.get(pk=competitor_a.competitor_id)
        competitor_a = competitor.title
    except:
        competitor_a = 'TBD'

    try:
        competitor = Competitor.objects.get(pk=competitor_b.competitor_id)
        competitor_b = competitor.title
        print(competitor.id)
    except:
        competitor_b = 'TBD'

    return render_to_response('api/matchup.html', {'a': competitor_a, 'b': competitor_b})
