from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#
#
def index_page(request):
    return render(request, 'api/index.html')

#
def bracket_view(request):
    return render(request, 'api/bracket_view.html')
