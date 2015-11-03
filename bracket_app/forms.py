from django import forms
from django.contrib.auth.models import User
from api.models import Competitor


class BracketForm(forms.ModelForm):

    class Meta:
        model = Competitor
        fields = ['title']
