from django.shortcuts import render

# Create your views here.


def bracket_view(request):
    return render(request, 'api/bracket_view.html')
