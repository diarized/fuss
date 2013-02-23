from views import player_registration, team_registration, thanks
from django.conf.urls import patterns, url
urlpatterns = patterns('',
        url(r'player_registration', player_registration),
        url(r'team_registration', team_registration),
        url(r'thanks', thanks),
)
