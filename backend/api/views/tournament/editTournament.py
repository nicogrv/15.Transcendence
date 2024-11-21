from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers.profileSerializer import ProfileSerializer
from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament
from .startTournament import startTournament
from api.models.tournamentMatch import tournamentMatch
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.decorators import api_view
import json


def getDataMatch(tournois, user):
	jsonData = []
	tournamentmatch = tournamentMatch.objects.filter(tournament=tournois)
	for match in tournamentmatch:
		tmpJson = match.json()
		if (match.player1 == user or match.player2 == user):
			tmpJson["hisMatch"] = True
		else:
			tmpJson["hisMatch"] = False
		jsonData.append(tmpJson)
	return jsonData


@api_view(['GET'])
def editTournament(req, id):
	if req.method != 'GET':
		return JsonResponse({"error" : "not get method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	try:
		tournois = Tournament.objects.get(id=id)
	except:
		return JsonResponse({"error" : "error"}, status=status.HTTP_200_OK)
	json_data = {}
	if req.user.id == tournois.admin.id:
		json_data["boolAdmin"] = True
	else:
		json_data["boolAdmin"] = False
	playerInTournament = playerTournament.objects.filter(Tournament=tournois)
	startTournament(tournois.id)
	json_data["match"] = {}

	json_data["match"] = getDataMatch(tournois, req.user)
	if (playerInTournament.count() != tournois.numberOfPlayerNow):
		tournois.numberOfPlayerNow = playerInTournament.count()
		tournois.save()
	json_data["players"] = {}
	json_data.update(tournois.json())
	for player_tournament in playerInTournament:
		json_data["players"][str(player_tournament.player.id)] = player_tournament.name
		if (tournois.admin == player_tournament.player):
			json_data["admin"] = player_tournament.name

	player_joining_name = next(
		(player_tournament.name for player_tournament in playerInTournament if player_tournament.player.id == req.user.id), None)

	for player_tournament in playerInTournament:
		if player_tournament.player.id != req.user.id:
			groupe_name = f'{player_tournament.player.id}'
			channel_layer = get_channel_layer()
			async_to_sync(channel_layer.group_send)(
				groupe_name,
				{
					"type": "player_joined_tournament",
					"message": f"Player {player_joining_name} has joined the tournament",
					"tournois_id": str(tournois.id),
					"numberOfPlayerNow": tournois.numberOfPlayerNow,
					"numberOfPlayer": tournois.numberOfPlayer,
					"players": json_data["players"]
				}
			)

	return JsonResponse({"ok" : json_data}, status=status.HTTP_200_OK)
