import controller
from django.conf.urls import patterns, url
urlpatterns = patterns('',
        url(r'^$', controller.index),
        url(r'^player_registration', controller.player_registration),
        url(r'^team_registration', controller.team_registration),
        url(r'^list_players', controller.list_players),
        url(r'^list_teams', controller.list_teams),
        url(r'^list_singlematches', controller.list_singlematches),
        url(r'^list_doublesmatches', controller.list_doublesmatches),
        url(r'^set_match_score/(?P<match_no>\d+)/$', controller.set_match_score),
        url(r'^thanks', controller.thanks),
)
