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
    url(r'^assign_competitor/(?P<competitor_id>.+)/(?P<user_id>.+)', views.assign_competitor, name="assign_competitor"),
    url('', include('social.apps.django_app.urls', namespace='social')),
]
