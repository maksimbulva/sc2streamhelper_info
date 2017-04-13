from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<character_id>\d+)/(?P<realm>\d+)/(?P<character_name>\w+)/mmr/(?P<race>\w+)$', views.mmr, name='mmr'),
    url(r'^update/(?P<ladder_id>\d+)$', views.update, name='update'),
    url(r'stats$', views.stats, name='stats')
]