from django.conf.urls import url
from . import views as views

urlpatterns = [
    url(r'^$', views.bracket_view, name='bracket_view'),
    url(r'^bracket/create$', views.bracket_create, name='bracket_create'),
]
