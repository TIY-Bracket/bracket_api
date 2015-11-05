from django.conf.urls import url
from . import views as views

urlpatterns = [
    # url(r'^home/', views.landing_page, name='landing_page'),
    # url(r'^$', views.bracket_view, name='bracket_view'),
    url(r'^$', views.index_page, name='index_page'),
]
