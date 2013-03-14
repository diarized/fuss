from django import forms
import models

class PlayerRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Player
        exclude = ('points', 'wins')


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Team
        exclude = ('points', 'wins')


class MatchScoringForm(forms.ModelForm):
    class Meta:
        model = models.Match
        exclude = ('finished', 'match_date')


class TournamentForm(forms.ModelForm):
    class Meta:
        model = models.Tournament
        exclude = ('date_created',)


class SingleMatchForm(forms.ModelForm):
    class Meta:
        model = models.SingleMatch
        fields = ('home', 'guest', 'tournament')


class DoublesMatchForm(forms.ModelForm):
    class Meta:
        model = models.DoublesMatch
        fields = ('home', 'guest', 'tournament')


