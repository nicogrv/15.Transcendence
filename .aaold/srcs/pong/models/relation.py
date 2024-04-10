import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .player import Player

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

    def getRelationOneToTwo(self):
        if self.one_to_two_relation == self.Status.NONE:
            return "None"
        elif self.one_to_two_relation == self.Status.FRIEND:
            return "Friends"
        elif self.one_to_two_relation == self.Status.BLOCKED:
            return "Blocked"
        else:
            return None

    def getRelationTwoToOne(self):
        if self.two_to_one_relation == self.Status.NONE:
            return "None"
        elif self.two_to_one_relation == self.Status.FRIEND:
            return "Friends"
        elif self.two_to_one_relation == self.Status.BLOCKED:
            return "Blocked"
        else:
            return None
