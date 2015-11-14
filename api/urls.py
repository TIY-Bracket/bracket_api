from django.conf.urls import url, include
from rest_framework import routers
from . import views as views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'bracket', views.BracketViewSet)
router.register(r'competitor', views.CompetitorViewSet)
router.register(r'position', views.PositionViewSet)


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^bracket_view/', views.bracket_view, name='bracket_view'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^new_bracket/', views.new_bracket, name="new_bracket"),
    url(r'^bracket/(?P<bracket_id>.+)', views.get_bracket, name="get_bracket"),
    url(r'^view/(?P<bracket_id>.+)', views.bracket_view, name="bracket_view"),
    url(r'^bracket_create/', views.bracket_create, name="bracket_create"),
    url(r'^update_bracket/(?P<bracket_id>.+)/(?P<competitor_id>.+)', views.update_bracket, name="update_bracket"),
    url(r'^winner/', views.winner_update, name="winner_update"),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^send_email/(?P<competitor_id>.+)', views.five_min_email, name="send_email"),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^matchup/(?P<bracket_id>.+)/(?P<parent_id>.+)', views.matchup, name="matchup"),
    url(r'^add_contact_email/(?P<competitor_id>.+)', views.add_contact_email, name="add_contact_email"),
]
