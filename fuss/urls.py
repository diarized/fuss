import controller
from django.conf.urls import patterns, url
urlpatterns = patterns('',
        url(r'^$', controller.index),
        url(r'^player_registration', controller.player_registration),
        url(r'^team_registration', controller.team_registration),
        url(r'^list_players', controller.list_players),
        url(r'^list_teams', controller.list_teams),
        url(r'^list/(?P<match_type>\w)/matches', controller.list_matches),
        url(r'^set/(?P<match_type>\w)/(?P<match_no>\d+)/score$', controller.set_match_score),
        url(r'^thanks', controller.thanks),
)
