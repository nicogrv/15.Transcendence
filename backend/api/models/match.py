from django.db import models
from api.models.playerModel import Player
import uuid
from datetime import datetime
from django.utils import timezone
from asgiref.sync import async_to_sync, sync_to_async
from api.utils import update_stats


class Match(models.Model):

	STATUS_CHOICES = [
		('WAITPLAYERS', 'Wait_players'),
		('GAMELAUNCH', 'game_launch'),
		('INGAME', 'ingame'),
		('FINISH', 'finish'),
	]
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1', null=True, blank=True) # change "CASCADE" to null
	player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2', null=True, blank=True )
	winner = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='winner', null=True, blank=True)
	score_player1 = models.PositiveIntegerField(default=0)
	score_player2 = models.PositiveIntegerField(default=0)
	create_time = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(auto_now=True)
	end_time = models.DateTimeField(auto_now=True)
	tournament = models.BooleanField(default=False, editable=False)
	local = models.BooleanField(default=False, editable=False)
	status = models.CharField(max_length=20, default='WAITPLAYERS', choices=STATUS_CHOICES)


	def __str__(self):
		noneUsername = "-_-"
		if (self.player1):
			username1 = self.player1.username
		else:
			username1 = noneUsername
		if (self.player2):
			username2 = self.player2.username
		else:
			username2 = noneUsername
		return "(" + str(self.score_player1) + ":" + str(self.score_player2) + ") " + username1 + " vs " +  username2 + f" ({self.uid})" + f"sta = {self.status} | T {self.tournament}"

	async def prt(self):
		noneUsername = "-_-"
		if (self.player1):
			username1 = self.player1.username
		else:
			username1 = noneUsername
		if (self.player2):
			username2 = self.player2.username
		else:
			username2 = noneUsername
		print("(" + str(self.score_player1) + ":" + str(self.score_player2) + ") " + username1 + " vs " +  username2 + f" ({self.uid})PRT")


	async def startGame(self):
		self.status = "INGAME"
		self.start_time = timezone.now()
		await sync_to_async(self.save)()

	async def deleteGame(self):
		await sync_to_async(self.delete)()
	
	async def endGame(self, score_player1, score_player2, winner):
		self.status = "FINISH"
		self.score_player1 = score_player1
		self.score_player2 = score_player2
		self.end_time = timezone.now()
		self.winner = winner
		await sync_to_async(self.save)()
		await update_stats(self.player1, self.player2, score_player1, score_player2, winner)




	def json(self):
		json = {
			"uid" : self.uid,
			"player1" : self.player1.__str__(),
			"player2" : self.player2.__str__(),
			"winner" : self.winner.__str__(),
			"score_player1" : self.score_player1,
			"score_player2" : self.score_player2,
			"create_time" : self.create_time,
			"start_time" : self.start_time,
			"end_time" : self.end_time,
			"tournament" : self.tournament,
			"status" : self.status,
		}
		return json

	def jsonWithoutTrueName(self, name1, name2, winner):
		json = {
			"uid" : self.uid,
			"player1" : name1,
			"player2" : name2,
			"winner" : winner,
			"score_player1" : self.score_player1,
			"score_player2" : self.score_player2,
			"create_time" : self.create_time,
			"start_time" : self.start_time,
			"end_time" : self.end_time,
			"tournament" : self.tournament,
			"status" : self.status,
		}
		return json
