from django.db import models


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
    def save(self, *args, **kwargs):
        super(Player, self).save(*args, **kwargs)
        players = Player.objects.exclude(nick=self.nick)
        if len(players) == 0:
            return
        for player in players:
            match = SingleMatch(
                    home = player,
                    guest = self
                )
            match.save()


class Team(Competitor):
    player1 = models.ForeignKey(Player, related_name="plyer_one")
    player2 = models.ForeignKey(Player, related_name="player_two")
    def __unicode__(self):
        return "{1}, {2}".format(self.player1.nick, self.player2.nick)


class Match(models.Model):
    home_result = models.IntegerField(null=True)
    guest_result = models.IntegerField(null=True)
    finished = models.BooleanField(default=False)
    def set_result(self, h, g):
        if self.finished:
            raise ValueError("Match already finished.")
        if h<0 or g<0:
            raise ValueError("Negative? Crushed to death?")
        self.home_result = h
        self.guest_result = g

        if h > g:
            self.winner = self.home
            self.home.wins += 1
        elif h < g:
            self.winner = self.guest
            self.guest.wins += 1
        else:
            raise ValueError("Sombody MUST win, sorry.")
        self.finished = True
#    class Meta:
#        abstract = True


class SingleMatch(Match):
    home = models.ForeignKey(Player, null=False, related_name="home")
    guest = models.ForeignKey(Player, null=False, related_name="guest")
    winner = models.ForeignKey(Player, null=True)
    class Meta:
        verbose_name_plural = "SingleMatches"


class DoublesMatch(Match):
    home = models.ForeignKey(Team, null=False, related_name="home")
    guest = models.ForeignKey(Team, related_name="guest")
    winner = models.ForeignKey(Team, null=True)
    class Meta:
        verbose_name_plural = "DoublesMatches"




