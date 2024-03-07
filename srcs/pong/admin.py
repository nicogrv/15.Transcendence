from .models.player import Player
from .models.tournament import Tournament
from .models.tournament_Player import Tournament_Player
from .models.match import Match
from .models.relation import Relation
from .models.message import Message
from django.contrib import admin

# Register your models here.
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Tournament_Player)
admin.site.register(Match)
admin.site.register(Relation)
admin.site.register(Message)