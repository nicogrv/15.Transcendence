import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
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
	email = models.EmailField(null=True, blank=True, unique=True)
	elo = models.IntegerField(default=0)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	status = models.IntegerField(choices=Status.choices, default=Status.OFFLINE)

	token_login = models.UUIDField(null=True, blank=True, unique=True)
	token_login_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	token_login_end_at = models.DateTimeField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	password = models.CharField(max_length=100, default=None)


	def update_token(self):
		new_token = uuid.uuid4()
		self.token_login = new_token
		self.token_login_created_at = timezone.now()
		self.token_login_end_at = timezone.now() + timedelta(days=1)  #1h de decalage horraire avec la db
		self.save()
		return new_token, timezone.now(), timezone.now() + timedelta(days=1)

	def __str__(self):
		if self.login_42:
			return self.username + f" ({self.login_42})"
		else:
			return self.username
	
	def checkPassword(self, password):
		if (check_password(password, self.getPassword())):
			return True
		else:
			return False

	def setPassword(self, password):
		self.password = make_password(password)
	
	def getUsername(self):
		return self.username;
	def getLogin(self):
		return self.login
	def getPassword(self):
		return self.password
	def getPic(self):
		return self.pic
	def getEmail(self):
		return self.email
	def getElo(self):
		return self.elo
	def getVictories(self):
		return self.victories
	def getDefeats(self):
		return self.defeats
	def getStatus(self):
		return self.status
	def getToken_login(self):
		return self.token_login
	def getToken_login_created_at(self):
		return self.token_login_created_at
	def getToken_login_end_at(self):
		return self.token_login_end_at
	def getCreated_at(self):
		return self.created_at
	def getUpdated_at(self):
		return self.updated_at
	class Meta:
		indexes = [
			models.Index(fields=['username'])
		]
