from fuss.models import Player, Team, SingleMatch, DebelMatch
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    readonly_fields=('points', 'wins')


class TeamAdmin(admin.ModelAdmin):
    readonly_fields=('number', 'points', 'wins')


class SingleMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


class DebelMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(SingleMatch, SingleMatchAdmin)
admin.site.register(DebelMatch, DebelMatchAdmin)
