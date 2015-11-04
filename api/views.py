from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def bracket_view(request):
    return render(request, 'api/bracket_view.html')


def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)
    return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
