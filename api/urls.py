from django.conf.urls import url
from . import views as views

urlpatterns = [
    url(r'^$', views.bracket_view, name='bracket_view'),
    url(r'^$', 'api.views.login'),
    url(r'^home/$', 'api.views.home'),
    url(r'^logout/$', 'api.views.logout')
]
