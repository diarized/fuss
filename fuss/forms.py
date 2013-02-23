from django import forms
from models import Player, Team

class PlayerRegistrationForm(forms.ModelForm):
    # nick = forms.CharField(max_length=32)
    # full_name = forms.CharField(max_length=255)
    # e_mail = forms.EmailField(required=False)
    # e_mail_me = forms.BooleanField(required=False)
    class Meta:
        model = Player
        exclude = ('points', 'wins')

class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ('points', 'wins')

