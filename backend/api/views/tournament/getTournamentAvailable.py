from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers.profileSerializer import ProfileSerializer
from api.models.tournament import Tournament
from django.conf import settings
from api.models.playerTournament import playerTournament
from api.models.playerModel import Player
from rest_framework import status
from rest_framework.decorators import api_view
import json


@api_view(['GET'])
def getTournamentAvailable(req):
	listWaitingPlayers = []
	listInProgress = []

	waiting_tournaments = Tournament.objects.filter(status=0)
	for tournoi in waiting_tournaments:
		tournoi_data = tournoi.json()
		players = playerTournament.objects.filter(Tournament=tournoi)
		tournoi_data['players'] = [{"id": player.player.id, "name": player.name} for player in players]
		listWaitingPlayers.append(tournoi_data)

	in_progress_tournaments = Tournament.objects.filter(status=1)
	for tournoi in in_progress_tournaments:
		players = playerTournament.objects.filter(Tournament=tournoi)
		if players.filter(player=req.user).exists():
			tournoi_data = tournoi.json()
			tournoi_data['players'] = [{"id": player.player.id, "name": player.name} for player in players]
			listInProgress.append(tournoi_data)
	data = {"waiting": listWaitingPlayers}
	if listInProgress:
		data["inProgress"] = listInProgress

	return JsonResponse({"ok" : data}, status=status.HTTP_200_OK)


