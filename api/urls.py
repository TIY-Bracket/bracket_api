from django.conf.urls import url
from . import views as views

urlpatterns = [
    url(r'^$', views.home, name='base.html'),
    # url(r'^$', views.bracket_view, name='bracket_view'),

]
