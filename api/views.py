from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#
#
def base_page(request):
    return render(request, 'api/base.html')

#
def bracket_view(request):
    return render(request, 'api/bracket_view.html')
