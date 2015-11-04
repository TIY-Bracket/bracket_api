from django import forms
from django.contrib.auth.models import User
from api.models import Competitor, Bracket


class CompetitorForm(forms.ModelForm):

    class Meta:
        model = Competitor
        fields = ['title']


class BracketForm(forms.ModelForm):

    class Meta:
        model = Bracket
        fields = ['title']
