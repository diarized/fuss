from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
import forms
import models
import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index')


def no_tournaments():
    open_tournaments = models.Tournament.objects.all()
    if len(open_tournaments) == 0:
        return True
    return False

def create_first_tournament():
    tr = models.Tournament(
            name = 'League',
            opened = True,
            )
    tr.save()
    return tr

def tournaments(request, tournament_id=None):
    if request.method == 'POST':
        form = forms.TournamentForm(request.POST)
        if form.is_valid():
            tr_name = form.cleaned_data['name']
            tr_opened = form.cleaned_data['opened']
            logger.debug("name = {0}, opened = {1}".format(tr_name, tr_opened))
            tr = models.Tournament(
                    name = tr_name,
                    opened = tr_opened,
                    )
            tr.save()
        else:
            return HttpResponseRedirect('/fuss/')
        return HttpResponseRedirect('/fuss/tournaments/')
    elif request.method == 'GET':
        form = forms.TournamentForm()
        if tournament_id:
            try:
                tournaments = models.Tournament.objects.all()
            except models.Tournament.DoesNotExist:
                create_first_tournament()
                tournaments = models.Tournament.objects.all()
            single_matches = models.SingleMatch.objects.filter(tournament=tournament_id)
            doubles_matches = models.DoublesMatch.objects.filter(tournament=tournament_id)
            #all_matches = [single_matches, doubles_matches]
            return render(request, 'tournaments.html', {
                'tournaments': tournaments,
                'singlematches': singlematches,
                'form': form,
                })
        else:
            tournaments = models.Tournament.objects.all()
            return render(request, 'tournaments.html', { 'tournaments': tournaments, 'form': form })
    else:
        raise ValueError("I cannot process {0} method.".format(request.method))


def singlematches(request, tournament_id=2):
    if request.method == 'POST':
        form = forms.SingleMatchForm(request.POST)
        if form.is_valid():
            player1 = form.cleaned_data['home']
            player2 = form.cleaned_data['guest']
            tournament = form.cleaned_data['tournament']
            tr = models.Tournament.objects.get(name=tournament)
            if player1 == player2:
                return render(request, 'error_message', {'message': "Do you have 4 hands?"})
            new_singlematch = models.SingleMatch(
                    home  = player1,
                    guest = player2,
                    tournament = tr,
                )
            new_singlematch.save()
            return HttpResponseRedirect('/fuss/singlematches/')
    else:
        form = forms.SingleMatchForm()

    if no_tournaments():
        create_first_tournament()
    singlematches = models.SingleMatch.objects.all()
    return render(request, 'singlematches.html',
            { 'form': form, 'singlematches': singlematches })


def doublesmatches(request, tournament_id=2):
    if request.method == 'POST':
        form = forms.DoublesMatchForm(request.POST)
        if form.is_valid():
            player1 = form.cleaned_data['home']
            player2 = form.cleaned_data['guest']
            tournament = form.cleaned_data['tournament']
            tr = models.Tournament.objects.get(name=tournament)
            if player1 == player2:
                return render(request, 'error_message', {'message': "Simply not possible."})
            new_doublesmatch = models.DoublesMatch(
                    home  = player1,
                    guest = player2,
                    tournament = tr,
                )
            new_doublesmatch.save()
            return HttpResponseRedirect('/fuss/doublesmatches/')
    else:
        form = forms.DoublesMatchForm()

    if no_tournaments():
        create_first_tournament()
    doublesmatches = models.DoublesMatch.objects.all()
    return render(request, 'doublesmatches.html',
            { 'form': form, 'doublesmatches': doublesmatches })


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
    order_by = request.GET.get('order_by', '-points')
    players = models.Player.objects.all().order_by(order_by)
    return render(request, 'list_players.html', {'players': players, 'player_type': 'player'})


def list_teams(request):
    order_by = request.GET.get('order_by', '-points')
    teams = models.Team.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', 'pk')
    all_matches = mt.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', '-points')
    players = models.Player.objects.all().order_by(order_by)
    return render(request, 'list_players.html', {'players': players, 'player_type': 'player'})


def list_teams(request):
    order_by = request.GET.get('order_by', '-points')
    teams = models.Team.objects.all().order_by(order_by)
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
    order_by = request.GET.get('order_by', 'pk')
    all_matches = mt.objects.all().order_by(order_by)
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


