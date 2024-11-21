from django.db import models
from api.models.playerModel import Player
import uuid


class FriendRequest(models.Model):
    """ 
    SENDER is the one who initiated the friend request 
    RECEIVER is the one who received the friend request 
    """
    NO_REQUEST_SENT = -1
    THEM_SENT_TO_YOU = 0
    YOU_SENT_TO_THEM = 1
    ACCEPTED = 2
    REJECTED = 3

    STATUS_CHOICES = [
        (NO_REQUEST_SENT, 'No Request Sent'),
        (THEM_SENT_TO_YOU, 'Them Sent to You'),
        (YOU_SENT_TO_THEM, 'You sent to them'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    ]
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Player, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Player, related_name='receiver', on_delete=models.CASCADE)
    status_request = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NO_REQUEST_SENT)


    def __str__(self):
        return f"FriendRequest(from {self.sender} to {self.receiver}) at {self.created_at}"
    
    
    def get_friend_request_or_false(sender, receiver):
        try:
            return FriendRequest.objects.get(sender=sender, receiver=receiver)
        except FriendRequest.DoesNotExist:
            return False
    