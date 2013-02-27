from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
import forms
import models

def index(request):
    return render(request, 'index')


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
            return HttpResponseRedirect('/fuss/list_players')
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
            if check_team(player1, player2):
                return render(request, 'error_message', {'message': "The players are in a team already."})
            new_team = models.Team(
                    player1   = player1,
                    player2   = player2,
                )
            new_team.save()
            return HttpResponseRedirect('/fuss/list_teams')
    else:
        form = forms.TeamRegistrationForm()

    teams = models.Team.objects.all()
    return render(request, 'team_registration',
            { 'form': form, 'teams': teams })


def check_team(p1, p2):
    return (check_player_teammate(p1, p2) or
        check_player_teammate(p2, p1))


def check_player_teammate(player, partner):
    try:
        models.Team.objects.get(player1=player, player2=partner)
    except ObjectDoesNotExist:
        return False
    return True


def list_players(request):
    players = models.Player.objects.all().order_by('-points')
    return render(request, 'list_players', {'players': players, 'player_type': 'player'})


def list_teams(request):
    teams = models.Team.objects.all().order_by('-points')
    return render(request, 'list_teams', {'teams': teams, 'player_type': 'team'})


def list_matches(request, match_type):
    if match_type == 's':
        mt = models.SingleMatch
        player_type = "player"
    elif match_type == 'd':
        mt = models.DoublesMatch
        player_type = "team"
    else:
        return render(request, 'error_message',
                {'message': "No such a match type: {0}".format(match_type)})
    all_matches = mt.objects.all()
    return render(request, 'list_matches', {'matches': all_matches, 'player_type': player_type })


def set_match_score(request, match_type, match_no):
    if match_type == 's':
        mt = models.SingleMatch
        player_type = "player"
    elif match_type == 'd':
        mt = models.DoublesMatch
        player_type = "team"
    else:
        return render(request, 'error_message',
                {'message': "No such a match type: {0}".format(match_type)})
    try:
        match = mt.objects.get(pk=match_no)
    except ObjectDoesNotExist:
        return render(request, 'error_message',
                {'message': "No such a match (number {0})".format(match_no)})

    if request.method == 'POST':
        form = forms.MatchScoringForm(request.POST)
        if form.is_valid():
            home_score = form.cleaned_data['home_result']
            guest_score = form.cleaned_data['guest_result']
            try:
                match.set_result(home_score, guest_score)
            except ValueError as e:
                return render(request, 'error_message', {'message': e})
            if player_type == "player":
                return HttpResponseRedirect('/fuss/list/s/matches')
            else:
                return HttpResponseRedirect('/fuss/list/d/matches')
    else:
        form = forms.MatchScoringForm()

    return render(request, 'set_match_score',
            { 'form': form, 'player_type': player_type, 'match': match })

    
def thanks(request):
    message = "Thank you for using this site."
    return render(request, 'thanks',  { 'message': message })


