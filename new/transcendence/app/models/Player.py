from django.db import models
from .choices import PLAYER_STATUS, PLAYER_STATUS_DEFAULT, PLAYER_RANKS_DEFAULT, PLAYER_RANKS, needed_length
from django.contrib.auth.models import User
from uuid import uuid4


def rename_profile_picture(instance, filename):
	upload_to = 'user_data/profile_picture/'
	extension = filename.split('.')[-1]
	filename = '{}.{}'.format(instance.uid, extension)
	return os.path.join(upload_to, filename)


def validate_profile_picture(image):
	print("faire validateur")

class Player(models.Model):
	
	
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	user = models.OneToOneField(User, null=True, blank=True, unique=True, on_delete=models.CASCADE)

	profile_picture = models.ImageField(upload_to=rename_profile_picture, validators=[validate_profile_picture], null=True, blank=True)

	player_status = models.CharField(max_length=needed_length(PLAYER_STATUS), choices=PLAYER_STATUS, default=PLAYER_STATUS_DEFAULT)

	player_elo = models.IntegerField(default=None, null=True, blank=True)

	player_rank = models.CharField(max_length=needed_length(PLAYER_RANKS), choices=PLAYER_RANKS, default=PLAYER_RANKS_DEFAULT)

	total_victories = models.IntegerField(default=0)

	total_defeats = models.IntegerField(default=0)

	total_matches = models.IntegerField(default=0)

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)
