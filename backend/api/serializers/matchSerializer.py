from rest_framework import serializers
from api.models.match import Match
from api.models.tournament import Tournament
from api.models.playerModel import Player

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['username']


class TournamentSerializer(serializers.ModelSerializer):
    tournament_players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = '__all__'
