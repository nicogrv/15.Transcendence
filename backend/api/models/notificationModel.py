from django.db import models
from api.models.playerModel import Player
import uuid


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="sender_notif")
    recipient = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="recipient_notif")
    message = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification from {self.sender} to {self.recipient} at {self.timestamp}'
