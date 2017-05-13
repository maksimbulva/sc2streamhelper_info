from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<character_id>\d+)/(?P<realm>\d+)/(?P<character_name>\w+)/profile$', views.profile, name='profile'),
    url(r'^(?P<character_id>\d+)/(?P<realm>\d+)/(?P<character_name>\w+)/mmr/(?P<race>\w+)$', views.mmr, name='mmr'),
    url(r'^lookup/(?P<character_name>\w+)/(?P<race>\w+)', views.lookup_mmr, name='lookup_mmr'),
    url(r'^update/(?P<ladder_id>\d+)$', views.update, name='update'),
    url(r'client_version', views.client_version, name='client_version'),
]