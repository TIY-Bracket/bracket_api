from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import UserSerializer, GroupSerializer, BracketSerializer, \
    CompetitorSerializer, PositionSerializer
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.views import generic
from api.models import Bracket, Competitor, Position, Chat
from twilio.rest import TwilioRestClient
import requests
from django.http import HttpResponseRedirect
import phonenumbers
from django.template import RequestContext

import pusher
from django.http import HttpResponse

p = pusher.Pusher(
        app_id='154316',
        key='bc4d80d7383e11cf31ec',
        secret='4271888d157f8c02fe3b'
    )


def chat_test(request):
    if not request.session.get('user'):
        request.session['user'] = 'user-%s' % request.session.session_key
    return render_to_response('api/chattest.html', {
                              'PUSHER_KEY': settings.PUSHER_KEY},
                              RequestContext(request))


def chat_message(request):
    try:
        username = str(request.user)
    except:
        username = None
    message = request.POST.get('message')
    bracket = Bracket.objects.get(pk=request.POST.get('bracket_id'))
    user = User.objects.get(pk=request.POST.get('user_id'))
    chat_message = Chat(text=message, bracket=bracket, user=user)
    chat_message.save()
    channel = 'bracket_chat' + str(bracket.id)
    p.trigger(channel, 'chat', {
        'message': request.POST.get('message'),
        'user': username,
    })
    return HttpResponse('')


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


class ChampListView(generic.ListView):
    template_name = 'api/champ.html'
    context_object_name = 'positions'
    paginate_by = 25


    def get_queryset(self):
        self.bracket = get_object_or_404(Bracket, pk=self.kwargs['pk'])
        self.champ = self.bracket.position_set.all().filter(position=1)
        return self.champ


class UserListView(generic.ListView):
    template_name = 'api/profile.html'
    context_object_name = 'brackets'
    paginate_by = 25

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.user.bracket_set.all().order_by('-timestamp')


class CompListView(generic.ListView):
    template_name = 'api/competitor_list.html'
    context_object_name = 'competitors'
    paginate_by = 25

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.user.competitor_set.all().order_by('-timestamp')


def index(request):
    return render(request, 'api/index.html')


def bracket_view(request, bracket_id):
    bracket = Bracket.objects.get(pk=bracket_id)
    positions = Position.objects.filter(bracket=bracket_id)
    num_competitors = int((len(positions)+1)/2)
    chat = Chat.objects.filter(bracket=bracket_id).order_by('timestamp')
    return render(request, 'api/bracket_view.html',
                  {"bracket_id": bracket_id,
                   "bracket": bracket,
                   "num_competitors": num_competitors,
                   'PUSHER_KEY': settings.PUSHER_KEY,
                   'chats': chat},)


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
        if request.user.id == 1:
            user_id = None
        else:
            user_id = request.user.id
        bracket = Bracket(title=json_obj['Title'], owner_id=user_id)
        bracket.save()
        for value in json_obj['Competitors']:
            competitor = Competitor(title=value['name'], email=value['email'], phone=value['phone'])
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
    competitor.phone = phone
    competitor.save()
    return Response(request.data)


@api_view(['PUT'])
def claim_competitor(request, competitor_id):
    user_id = request.data["user_id"]
    competitor = Competitor.objects.get(pk=competitor_id)
    competitor.user_id = user_id
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
    bracket_id = position.bracket_id
    position = position.parent

    email_url = "https://tiy-bracket.herokuapp.com/view/" + str(bracket_id)
    email_message = "Your match starts now. Good luck! \n Your bracket: {}".format(email_url)

    results = requests.post(
        "https://api.mailgun.net/v3/sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org/messages",
        auth=("api", MAILGUN_KEY),
        data={"from": "Bracket Guys <mailgun@sandbox652a32e0480e41d5a283a133bcc7e501.mailgun.org>",
              "to": email_address,
              'subject': 'versus.live: Your matchup starts in 5 mins',
              'text': email_message})

    return HttpResponseRedirect("/matchup/" + str(bracket_id) + "/" + str(position))


def contact(request):
    return render(request, 'api/contact.html')


def five_min_text(request, competitor_id):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    position_data = Position.objects.filter(competitor_id=competitor_id)
    competitor = Competitor.objects.get(pk=competitor_id)
    number = str(competitor.phone)
    phone_number = "+1"+number
    position = position_data[0]

    bracket_id = position.bracket_id
    position = position.parent

    # Your Account Sid and Auth Token from twilio.com/user/account
    client = TwilioRestClient(account_sid, auth_token)
    sms_url = "https://tiy-bracket.herokuapp.com/view/" + str(bracket_id)
    sms_message = "Your match starts now. Good luck! \n Your bracket: {}".format(sms_url)

    message = client.messages.create(body=sms_message ,
                                     to=phone_number,
                                     from_="+19196959988",)

    return HttpResponseRedirect("/matchup/" + str(bracket_id) + "/" + str(position))


def caller_validate(phone_number):
    # To find these visit https://www.twilio.com/user/account
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN

    client = TwilioRestClient(account_sid, auth_token)
    response = client.caller_ids.validate(phone_number)


def matchup(request, bracket_id, parent_id):
    bracket = Bracket.objects.get(pk=bracket_id)
    bracket_owner = bracket.owner_id
    bracket_permissions = True

    if bracket_owner != request.user.id and bracket_owner is not None:
        bracket_permissions = False

    comm_permissions = True

    if bracket_owner is None:
        comm_permissions = False

    # Pulling back competitors in matchup
    competitors = Position.objects.filter(bracket_id=bracket_id, parent=parent_id)

    # Get Competitor a object
    competitor_a = competitors[0]

    # Setting the competitor a id from the competitor a object
    competitor_a_id = competitor_a.competitor_id

    # Get competitor a object and set attributes
    try:
        comp_a = Competitor.objects.get(pk=competitor_a_id)
        competitor_a_email = comp_a.email
        competitor_a_phone = comp_a.phone
    except:
        comp_a = None
        competitor_a_email = None
        competitor_a_phone = None

    competitor_b = competitors[1]
    competitor_b_id = competitor_b.competitor_id

    try:
        comp_b = Competitor.objects.get(pk=competitor_b_id)
        competitor_b_email = comp_b.email
        competitor_b_phone = comp_b.phone
    except:
        comp_b = None
        competitor_b_email = None
        competitor_b_phone = None

    winner_obj = Position.objects.filter(bracket_id=bracket_id, position=parent_id)
    winner = winner_obj[0].competitor_id

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

    return render_to_response('api/matchup.html',
                              {'a': competitor_a, 'b': competitor_b,
                               'a_id': competitor_a_id, 'b_id': competitor_b_id,
                               'bracket_id': bracket_id, 'a_email': competitor_a_email,
                               'b_email': competitor_b_email, 'parent_id': parent_id,
                               'comp_a': comp_a, 'comp_b': comp_b,
                               'bracket_permissions': bracket_permissions,
                               'comm_permissions': comm_permissions,
                               'winner': winner,
                               'b_phone': competitor_b_phone,
                               'a_phone': competitor_a_phone},
                              context_instance=RequestContext(request))
