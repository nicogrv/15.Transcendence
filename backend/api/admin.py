from django.contrib import admin
from api.models.playerModel import Player, PlayerAdmin
from api.models.friendRequestModel import FriendRequest
from api.models.notificationModel import Notification
from api.models.match import Match
from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament
from api.models.tournamentMatch import tournamentMatch
from api.models.twoFactorAuthentication import TwoFactorAuthentication

from django.contrib.auth.admin import UserAdmin

class PlayerAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'date_joined',
        'last_login',
        'status_profile'
        ]
    search_fields = ['username', 'email']
    readonly_fields = ['id', 'date_joined', 'last_login']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Player, PlayerAdmin)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(Match)
admin.site.register(playerTournament)
admin.site.register(Tournament)
admin.site.register(tournamentMatch)
admin.site.register(TwoFactorAuthentication)
