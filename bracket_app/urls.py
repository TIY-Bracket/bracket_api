from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import urls as api_urls
# from api import views as views

# from api.views import hello

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(api_urls)),
)
