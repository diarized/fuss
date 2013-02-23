from django.db import models

# Create your models here.

class Competitor(models.Model):
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)


class Player(Competitor):
    nick = models.CharField(max_length=32, null=False, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    e_mail = models.EmailField(null=True, blank=True, unique=True)
    e_mail_me = models.BooleanField(default=False)
    def __unicode__(self):
        return self.nick


class Team(Competitor):
    #number = models.IntegerField(primary_key=True)
    player1 = models.ForeignKey(Player, related_name="plyer_one")
    player2 = models.ForeignKey(Player, related_name="player_two")
    def __unicode__(self):
        return "Team: {1}, {2}".format(self.player1.nick, self.player2.nick)


class Match(models.Model):
    home_result = models.IntegerField()
    guest_result = models.IntegerField()
    finished = models.BooleanField(default=False)
    def set_result(self, h, g):
        if self.finished:
            raise Exception, "Match already finished."
        self.home_result = h
        self.guest_result = g

        if h > g:
            self.winner = h
            self.home.wins += 1
        elif h < g:
            self.winner = g
            self.guest.wins += 1
        self.finished = True
    class Meta:
        abstract = True


class SingleMatch(Match):
    home = models.ForeignKey(Player, null=False, related_name="home")
    guest = models.ForeignKey(Player, related_name="guest")
    winner = models.ForeignKey(Player, null=True)
    class Meta:
        verbose_name_plural = "SingleMatches"


class DebelMatch(Match):
    home = models.ForeignKey(Team, null=False, related_name="home")
    guest = models.ForeignKey(Team, related_name="guest")
    winner = models.ForeignKey(Team, null=True)
    class Meta:
        verbose_name_plural = "DebelMatches"

