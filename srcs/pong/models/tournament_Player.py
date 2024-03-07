import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .player import Player
from .tournament import Tournament
# Create your models here.
class Tournament_Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_player = models.ForeignKey(Player, related_name='uid_player_set', on_delete=models.SET_NULL, null=True)
	uid_tournament = models.ForeignKey(Tournament, related_name='uid_tournament_set', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		if self.uid_player:
			return self.uid_player.username + " : " + self.uid
		else:
			return f"{self.uid}"

