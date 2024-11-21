from django.contrib.auth.hashers import make_password, check_password
from api.models.playerModel import Player
from api.models.match import Match
from django.db import models
import uuid


class Tournament(models.Model):
    class STATUS(models.IntegerChoices):
        WAITINGPLAYERS = 0, 'WaitingPLayers'
        INPROGRESS = 1, 'InProgress'
        END = 2, 'End'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=24, blank=False, null=False)
    numberOfPlayer = models.PositiveIntegerField(blank=False, null=False, default=2)
    numberOfPlayerNow = models.PositiveIntegerField(blank=False, null=False, default=0)
    admin = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=False)
    tournament_players = models.ManyToManyField(Player, through='PlayerTournament', related_name='tournament_players')
    winner = models.CharField(max_length=100, blank=False, null=False)

    password = models.CharField(max_length=100, null=True)
    timeBetweenMatches  = models.PositiveIntegerField(blank=False, null=False, default=3)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.WAITINGPLAYERS)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", null=True, blank=True)

    def setPassword(self, password):
        self.password = make_password(password)

    def __str__(self):
        if self:
            if (self.password == None):
                password = "False"
            else:
                password = "True"
            return f"{self.name} |N {self.numberOfPlayer} |T {self.timeBetweenMatches} |P {password} |S {self.status}|ID {self.id}"

    def json(self):
        if (self.password == None):
            password = "False"
        else:
            password = "True"

        json = {
            "id": self.id,
            "name" : self.name,
            "numberOfPlayer" : self.numberOfPlayer,
            "numberOfPlayerNow" : self.numberOfPlayerNow,
            "admin" : self.admin.username,
            "password" : password,
            "timeBetweenMatches"  : self.timeBetweenMatches,
            "status" : next((status.label for status in Tournament.STATUS if status.value == self.status), None),
            "date_joined" : self.date_joined,
            "last_login" : self.last_login,
        }

        return json

    def def_INPROGRESS(self):
        self.status = self.STATUS.INPROGRESS
        self.save(update_fields=['status'])

    def def_END(self):
        print("def end")
        self.status = self.STATUS.END
        self.save(update_fields=['status'])
