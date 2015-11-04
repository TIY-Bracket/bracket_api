from django.http import HttpResponse
from django.shortcuts import render
from bracket_app.forms import CompetitorForm, BracketForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Competitor

# Create your views here.


def bracket_view(request):
    return render(request, 'api/bracket_view.html')


def bracket_create(request):
    if request.method == 'POST':
        competitorform = CompetitorForm(request.POST)
        bracketform = BracketForm(request.POST)
        if competitorform.is_valid() and bracketform.is_valid():
            competitor = competitorform.save(commit=False)
            # competitor.user = request.user
            competitor.save()

            bracket = bracketform.save(commit=False)
            bracket.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Bracket Created.')
            return redirect('bracket_view')

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Form data invalid.')

    else:
        competitorform = CompetitorForm()
        bracketform = BracketForm()
    return render(request,
                  'api/bracket_create.html',
                  {'bracketform': bracketform,
                   'competitorform': competitorform})
