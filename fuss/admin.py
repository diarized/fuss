from fuss import models
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    readonly_fields=('name', 'opened')


class PlayerAdmin(admin.ModelAdmin):
    readonly_fields=('points', 'wins')


class TeamAdmin(admin.ModelAdmin):
    readonly_fields=('points', 'wins')


class SingleMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


class DoublesMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.SingleMatch, SingleMatchAdmin)
admin.site.register(models.DoublesMatch, DoublesMatchAdmin)
