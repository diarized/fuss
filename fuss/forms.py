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
        exclude = ('finished',)


class TournamentForm(forms.ModelForm):
    class Meta:
        model = models.Tournament
        exclude = ('date_created',)


class SingleMatchForm(forms.ModelForm):
    class Meta:
        model = models.SingleMatch
        fields = ('home', 'guest', 'tournament')


