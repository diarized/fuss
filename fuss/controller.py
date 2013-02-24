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
            return HttpResponseRedirect('/fuss/list_singlematches')
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
            return HttpResponseRedirect('/fuss/list_doublesmatches')
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


def list_singlematches(request):
    all_matches = models.SingleMatch.objects.all()
    #return render(request, 'list_singlematches', {'matches': all_matches})
    return render(request, 'list_matches', {'matches': all_matches, 'player_type': 'player' })


def list_doublesmatches(request):
    all_matches = models.DoublesMatch.objects.all()
    return render(request, 'list_matches', {'matches': all_matches, 'player_type': 'team' })


def set_match_score(request, match_no):
    try:
        match = models.SingleMatch.objects.get(pk=match_no)
    except ObjectDoesNotExist:
        try:
            match = models.DoublesMatch.objects.get(pk=match_no)
        except ObjectDoesNotExist:
            return render(request, 'error_message',
                    {'message': "No such a match (number {0})".format(match_no)})
        else:
            player_type = "team"
    else:
        player_type = "player"

    if request.method == 'POST':
        form = forms.MatchScoringForm(request.POST)
        if form.is_valid():
            home_score = form.cleaned_data['home_result']
            guest_score = form.cleaned_data['guest_result']
            try:
                match.set_result(home_score, guest_score)
            except ValueError as e:
                return render(request, 'error_message', {'message': e})
            message = """Thank you for the game!
            Now you can review status of the turnament"""
            return render(request, 'thanks', { 'message': message })
    else:
        form = forms.MatchScoringForm()

    return render(request, 'set_match_score',
            { 'form': form, 'player_type': player_type, 'match': match })

    


def thanks(request):
    message = "Thank you for using this site."
    return render(request, 'thanks',  { 'message': message })

