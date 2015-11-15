from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import UserSerializer, GroupSerializer, BracketSerializer, \
    CompetitorSerializer, PositionSerializer
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from api.models import Bracket, Competitor, Position
from twilio.rest import TwilioRestClient
import requests
from django.http import HttpResponseRedirect
import phonenumbers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BracketViewSet(viewsets.ModelViewSet):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer


class PositionViewSet(viewsets.ModelViewSet):
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
def winner_update(request):
    bracket_id = request.data["bracket_id"]
    position = request.data["position"]
    if request.data["competitor_id"] == "":
        competitor_id = None
    else:
        competitor_id = request.data["competitor_id"]
    position = Position.objects.filter(bracket_id=bracket_id, position=position)
    position.competitor_id = competitor_id
    position.update(competitor_id=competitor_id)
    return Response(request.data)


@api_view(['PUT'])
def add_contact_email(request, competitor_id):
    email = request.data["email"]
    competitor = Competitor.objects.get(pk=competitor_id)
    competitor.email = email
    competitor.save()
    return Response(request.data)


@api_view(['PUT'])
def add_contact_phone(request, competitor_id):
    phone = request.data["phone"]
    competitor = Competitor.objects.get(pk=competitor_id)
    competitor.phone = "+1" + phone
    competitor.save()
    return Response(request.data)


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

    return HttpResponseRedirect("/contacts")
    return Response('hello')


def five_min_email(request, competitor_id):
    MAILGUN_KEY = settings.MAILGUN_KEY
    competitor = Competitor.objects.get(pk=competitor_id)
    email_address = competitor.email
    position_data = Position.objects.filter(competitor_id=competitor_id)
    position = position_data[0]
    bracket_id = str(position.bracket_id)
    comp_position = str(position.position)

    results = requests.post(
        "https://api.mailgun.net/v3/sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org/messages",
        auth=("api", MAILGUN_KEY),
        data={"from": "Bracket Guys <mailgun@sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org>",
              "to": email_address,
              'subject': 'versus.live: Your matchup starts in 5 mins',
              'text': 'Your matchup starts in 5 minutes! Good luck!'})

    return HttpResponseRedirect("/matchup/" + bracket_id + "/" + position)


def contact(request):
    return render(request, 'api/contact.html')


def five_min_text(request, competitor_id):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    position_data = Position.objects.filter(competitor_id=competitor_id)
    competitor = Competitor.objects.get(pk=competitor_id)
    phone_number = str(competitor.phone)
    print(phone_number)
    position = position_data[0]
    print("here")
    print(position.position)
    bracket_id = str(position.bracket_id)
    comp_position = str(position.position)

    # Your Account Sid and Auth Token from twilio.com/user/account
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="hello world",
                                     to=phone_number,
                                     from_="+19196959988",)


def caller_validate(phone_number):
    # To find these visit https://www.twilio.com/user/account
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN

    client = TwilioRestClient(account_sid, auth_token)
    response = client.caller_ids.validate(phone_number)


def matchup(request, bracket_id, parent_id):
    competitors = Position.objects.filter(bracket_id=bracket_id, parent=parent_id)
    competitor_a = competitors[0]
    competitor_a_id = competitor_a.competitor_id
    comp_a = Competitor.objects.get(pk=competitor_a_id)
    competitor_a_email = comp_a.email
    competitor_a_phone = comp_a.phone
    competitor_b = competitors[1]
    competitor_b_id = competitor_b.competitor_id
    comp_b = Competitor.objects.get(pk=competitor_b_id)
    competitor_b_email = comp_b.email
    competitor_b_phone = comp_b.phone
    winner_obj = Position.objects.filter(bracket_id=bracket_id, position=parent_id)
    winner = winner_obj[0].competitor_id
    print(winner)

    try:
        competitor = Competitor.objects.get(pk=competitor_a.competitor_id)
        competitor_a = competitor.title
    except:
        competitor_a = 'TBD'

    try:
        competitor = Competitor.objects.get(pk=competitor_b.competitor_id)
        competitor_b = competitor.title
    except:
        competitor_b = 'TBD'

    return render_to_response('api/matchup.html', {'a': competitor_a, 'b': competitor_b,
                                                'a_id': competitor_a_id, 'b_id': competitor_b_id,
                                                'bracket_id': bracket_id, 'a_email': competitor_a_email,
                                                'b_email': competitor_b_email, 'parent_id': parent_id,
                                                'b_phone': competitor_b_phone, 'a_phone': competitor_a_phone,
                                                'winner': winner})
