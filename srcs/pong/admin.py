from .models import Player, Tournament, Tournament_Player, Match, Relation, Message
from django.contrib import admin

# Register your models here.
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Tournament_Player)
admin.site.register(Match)
admin.site.register(Relation)
admin.site.register(Message)