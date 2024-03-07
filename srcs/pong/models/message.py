import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .player import Player

# Create your models here.
class Message(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	uid_sender = models.ForeignKey(Player, related_name='uid_sender_set', on_delete=models.CASCADE, null=True)
	uid_receiver = models.ForeignKey(Player, related_name='uid_receiver_set', on_delete=models.CASCADE, null=True)
	visible = models.BooleanField(default=1)
	sended_at = models.DateTimeField(auto_now_add=True)