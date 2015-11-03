from django.http import HttpResponse
from django.shortcuts import render
from bracket_app.forms import BracketForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Competitor

# Create your views here.


def bracket_view(request):
    return render(request, 'api/bracket_view.html')


def bracket_create(request):
    if request.method == 'POST':
        form = BracketForm(request.POST)
        if form.is_valid():
            competitor = form.save(commit=False)
            competitor.user = request.user
            competitor.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Bracket Created.')
            return redirect('bracket_view')

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Form data invalid.')

    else:
        form = BracketForm()
    return render(request,
                  'api/bracket_create.html',
                  {'form': form})
