from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import urls as api_urls
#from api import views as views
import api.views as aviews


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(api_urls)),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^home/', aviews.index, name='index'),
    # url(r'^$', 'api.views.login'),
    # url(r'^home/$', 'api.views.home'),
    url(r'^logout/$', aviews.logout, name='logout'),


)
