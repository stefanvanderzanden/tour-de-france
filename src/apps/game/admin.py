from django.contrib import admin
from game.models import Renner, Team, Etappe

class RennerAdmin(admin.ModelAdmin):
    list_display = ['naam', 'team', 'nummer']
    search_fields = ['naam', 'team__naam']
    ordering = ['nummer']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['naam']

class EtappeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Renner, RennerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Etappe, EtappeAdmin)