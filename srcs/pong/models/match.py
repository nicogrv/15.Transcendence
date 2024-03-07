import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .player import Player
from .tournament import Tournament

# Create your models here.
class Match(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_player_one = models.ForeignKey(Player, related_name='uid_player_one_set', on_delete=models.SET_NULL, null=True)
	uid_player_two = models.ForeignKey(Player, related_name='uid_player_two_set', on_delete=models.SET_NULL, null=True)
	points_player_one = models.IntegerField(default=0)
	points_player_two = models.IntegerField(default=0)
	uid_winner = models.ForeignKey(Player, related_name='uid_winner_set', on_delete=models.SET_NULL, null=True, blank=True)

	uid_tournament = models.ForeignKey(Tournament, related_name='tournament_set', on_delete=models.SET_NULL, null=True, blank=True)
	xpos_tournament = models.IntegerField(null=True, blank=True)
	ypos_tournament = models.IntegerField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True, blank=True)
	ended_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		if self.uid_player_one and self.uid_player_two:
			return self.uid_player_one.username + " vs " + self.uid_player_two.username + f" ({self.uid})"
		else:
			return f"{self.uid}"
