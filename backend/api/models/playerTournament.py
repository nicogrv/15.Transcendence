from api.models.playerModel import Player
from api.models.tournament import Tournament
from django.db import models
import uuid


class playerTournament(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=False)
    Tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=24, blank=False, null=False, default="=-= ERROR NAME =-=")
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)

    def __str__(self):
        if self:
            return f"{self.player.username} ({self.name}) -> {self.Tournament.name}"