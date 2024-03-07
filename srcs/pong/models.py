import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class Player(models.Model):
	class Status(models.IntegerChoices):
		OFFLINE = 0, 'Offline'
		ONLINE = 1, 'Online'
		PLAYING = 2, 'Playing'

	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	username = models.SlugField(max_length=24, unique=True)
	login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)
	pic = models.TextField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	elo = models.IntegerField(default=0)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	status = models.IntegerField(choices=Status.choices, default=Status.OFFLINE)

	token_login = models.UUIDField(null=True, blank=True, unique=True)
	token_login_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	token_login_end_at = models.DateTimeField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def update_token(self):
		new_token = uuid.uuid4()
		self.token_login = new_token
		self.token_login_created_at = timezone.now()
		self.token_login_end_at = timezone.now() + timedelta(days=1)  #1h de decalage horraire avec la db
		self.save()
		print(new_token)
		return new_token

	def __str__(self):
		if self.login_42:
			return self.username + f" ({self.login_42})"
		else:
			return self.username
		
	class Meta:
		indexes = [
			models.Index(fields=['username'])
		]

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


class Tournament_Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_player = models.ForeignKey(Player, related_name='uid_player_set', on_delete=models.SET_NULL, null=True)
	uid_tournament = models.ForeignKey(Tournament, related_name='uid_tournament_set', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		if self.uid_player:
			return self.uid_player.username + " : " + self.uid
		else:
			return f"{self.uid}"

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

class Relation(models.Model):
	class Status(models.IntegerChoices):
		NONE = 0, 'None'
		FRIEND = 1, 'Friend'
		BLOCKED = 2, 'Blocked'

	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_user_one = models.ForeignKey(Player, related_name='uid_user_one_set', on_delete=models.CASCADE, null=True)
	uid_user_two = models.ForeignKey(Player, related_name='uid_user_two_set', on_delete=models.CASCADE, null=True)
	one_to_two_relation = models.IntegerField(choices=Status.choices, default=Status.NONE)
	two_to_one_relation = models.IntegerField(choices=Status.choices, default=Status.NONE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		if self.uid_user_one and self.uid_user_two:
			return self.uid_user_one.username + " - " + self.uid_user_two.username
		else:
			return f"{self.uid}"

class Message(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_sender = models.ForeignKey(Player, related_name='uid_sender_set', on_delete=models.CASCADE, null=True)
	uid_receiver = models.ForeignKey(Player, related_name='uid_receiver_set', on_delete=models.CASCADE, null=True)
	visible = models.BooleanField(default=1)
	sended_at = models.DateTimeField(auto_now_add=True)