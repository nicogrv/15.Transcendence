from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from api.serializers.profileSerializer import ProfileSerializer
from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament
from .startTournament import startTournament
from rest_framework import status
from rest_framework.decorators import api_view
import json


@api_view(['POST'])
def joinTournament(req):
	data = req.data
	print("join tourn id = ", data["id"])
	print("join tourn alias = ", data["alias"])
	try:
		tournois = Tournament.objects.get(id=data["id"])
	except Exception as e:
		print(e)
	for _ in data:
		print(_)
	player_in_tournament = playerTournament.objects.filter(Tournament=tournois, player=req.user).exists()
	if player_in_tournament:
		return JsonResponse({"ok": "Already part of the tournament"}, status=status.HTTP_200_OK)
	if (tournois.numberOfPlayerNow >= tournois.numberOfPlayer and playerTournament.objects.filter(Tournament=tournois).count() >= tournois.numberOfPlayer):
		return JsonResponse({"error" : "tournois is full"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	elif not ((tournois.password == None or check_password(data["password"], tournois.password))):
		return JsonResponse({"error" : "bad password"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	alias_exists = playerTournament.objects.filter(Tournament=tournois, name=data["alias"]).exists()
	if alias_exists:
		return JsonResponse({"error": "Alias already used in this tournament"}, status=status.HTTP_400_BAD_REQUEST)

	try:
		playerTournament.objects.create(player=req.user, Tournament=tournois, name=data["alias"])
		tournois.numberOfPlayerNow = playerTournament.objects.filter(Tournament=tournois).count()
		tournois.save()
		startTournament(tournois.id)
		return JsonResponse({"ok" : "ok"}, status=status.HTTP_200_OK)
	except Exception as e:
		tournois.numberOfPlayerNow = playerTournament.objects.filter(Tournament=tournois).count()
		tournois.save()
		return JsonResponse({"error" : "error retry"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)