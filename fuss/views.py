from django.shortcuts import render
from django.http import HttpResponseRedirect
import forms
import models

def player_registration(request):
    if request.method == 'POST':
        form = forms.PlayerRegistrationForm(request.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            full_name = form.cleaned_data['full_name']
            e_mail = form.cleaned_data['e_mail']
            e_mail_me = form.cleaned_data['e_mail_me']
            new_player = models.Player(
                    nick=nick,
                    full_name=full_name,
                    e_mail=e_mail,
                    e_mail_me=e_mail_me
                )
            new_player.save()
            # mailing_list.append(e_mail)
            return HttpResponseRedirect('/fuss/thanks/')
    else:
        form = forms.PlayerRegistrationForm()

    return render(request, 'player_registration', 
            { 'form': form })


def team_registration(request):
    if request.method == 'POST':
        form = forms.TeamRegistrationForm(request.POST)
        if form.is_valid():
            player1 = form.cleaned_data['player1']
            player2 = form.cleaned_data['player2']
            if player1 == player2:
                return render(request, 'error_message', {'message': "Do you have 4 hands?"})
            new_team = models.Team(
                    player1=player1,
                    player2=player2,
                )
            new_team.save()
            message = """Thank you for joining the team.
            Now you can review status of the turnament"""
            return render(request, 'thanks', { 'message': message })
    else:
        form = forms.TeamRegistrationForm()

    teams = models.Team.objects.all()
    return render(request, 'team_registration',
            { 'form': form, 'teams': teams })



def thanks(request):
    message = "Thank you for using this site."
    return render(request, 'thanks',  { 'message': message })
