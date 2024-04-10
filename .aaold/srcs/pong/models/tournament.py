import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .player import Player
# Create your models here.
class Tournament(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_operator = models.ForeignKey(Player, related_name='uid_operator_set', on_delete=models.SET_NULL, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True, blank=True)
	ended_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		if self.uid_player:
			return self.uid_player.username + " : " + self.uid
		else:
			return f"{self.uid}"
