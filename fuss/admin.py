from fuss.models import Player, Team, SingleMatch, DoublesMatch
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    readonly_fields=('points', 'wins')


class TeamAdmin(admin.ModelAdmin):
    readonly_fields=('points', 'wins')


class SingleMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


class DoublesMatchAdmin(admin.ModelAdmin):
    readonly_fields=('winner',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(SingleMatch, SingleMatchAdmin)
admin.site.register(DoublesMatch, DoublesMatchAdmin)
