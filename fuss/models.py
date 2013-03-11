from django.db import models
from django.dispatch import receiver


class Tournament(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    opened = models.BooleanField(default=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)


class Competitor(models.Model):
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    class Meta:
        abstract = True


class Player(Competitor):
    nick = models.CharField(max_length=32, null=False, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    e_mail = models.EmailField(null=True, blank=True)
    e_mail_me = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nick

    def get_name(self):
        return self.__unicode__()


class Team(Competitor):
    player1 = models.ForeignKey(Player, related_name="plyer_one")
    player2 = models.ForeignKey(Player, related_name="player_two")

    def __unicode__(self):
        return "{0}, {1}".format(self.player1.nick, self.player2.nick)

    def __str__(self):
        return self.__unicode__()

    def get_name(self):
        return "{0}, {1}".format(self.player1.nick, self.player2.nick)


class Match(models.Model):
    home_result = models.IntegerField(null=True)
    guest_result = models.IntegerField(null=True)
    finished = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament, null=False)

    def set_result(self, h, g):
        if self.tournament.finished:
            raise ValueError("The tournament the match belongs to is finished already.")
        match_type = type(self)
        if self.finished is True:
            raise ValueError("Match already finished.".format(match_type))
        if h<0 or g<0:
            raise ValueError("Negative? Crushed to death?")

        if h > g:
            self.winner = self.home
        elif h < g:
            self.winner = self.guest
        else:
            raise ValueError("No mercy, sombody MUST win. Sorry.")
        self.home_result = h
        self.guest_result = g
        self.home.points += h
        self.guest.points += g
        self.home.save()
        self.guest.save()
        self.winner.wins += 1
        self.winner.save()
        self.finished = True
        self.save()

    class Meta:
        abstract = True


class SingleMatch(Match):
    home = models.ForeignKey(Player, null=False, related_name="home")
    guest = models.ForeignKey(Player, null=False, related_name="guest")
    winner = models.ForeignKey(Player, null=True)

    class Meta:
        verbose_name_plural = "SingleMatches"


class DoublesMatch(Match):
    home = models.ForeignKey(Team, null=False, related_name="home")
    guest = models.ForeignKey(Team, null=False, related_name="guest")
    winner = models.ForeignKey(Team, null=True)

    class Meta:
        verbose_name_plural = "DoublesMatches"


def match_exists(player, opponent):
    player_type = type(player)
    if player_type == Player:
        match_type = SingleMatch
    elif player_type == Team:
        match_type = DoublesMatch
    else:
        raise TypeError("Don't know player type {0}".format(player_type))

    try:
        match_type.objects.get(home=player, guest=opponent)
    except match_type.DoesNotExist:
        try:
            match_type.objects.get(home=opponent, guest=player)
        except match_type.DoesNotExist:
            return False
    return True


def create_match(player, opponent):
    player_type = type(player)
    if player_type == Player:
        match_type = SingleMatch
    elif player_type == Team:
        match_type = DoublesMatch
    else:
        raise TypeError("Don't know player type {0}".format(player_type))

    match = match_type(home=player, guest=opponent)
    match.save()


def check_matches_list(players):
    for player in players:
        for opponent in (o for o in players if o is not player):
            if not match_exists(player, opponent):
                create_match(player, opponent)
 

@receiver(models.signals.post_save, sender=Team)
@receiver(models.signals.post_save, sender=Player)
def check_singlematches_list(sender, **kwargs):
    players = sender.objects.all()
    check_matches_list(players)


