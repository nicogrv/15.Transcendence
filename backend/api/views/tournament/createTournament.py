from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers.profileSerializer import ProfileSerializer
from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
import json


list = [2, 4, 8, 16, 32, 64]

@api_view(['POST'])
def createTournament(req):
	if req.method == 'POST':
		try:
			formValue = req.data
			for _ in formValue:
				print(_)
			tournois = Tournament()
			if ("password" in formValue and formValue["password"] != formValue["confirmPassword"]):
				return JsonResponse({"error":"not same password"}, status=status.HTTP_200_OK)
			if ("passwordSwitch" in formValue):
				tournois.setPassword(formValue["password"])
			if not (int(formValue["numberOfPlayers"]) in list):
				return JsonResponse({"error":"number of player is not good (2, 4, 8, 16, 32, 64)"}, status=status.HTTP_200_OK)
			tournois.name = formValue["tournamentName"]
			tournois.numberOfPlayer = formValue["numberOfPlayers"]
			tournois.numberOfPlayerNow = tournois.numberOfPlayerNow + 1
			tournois.admin = req.user
			print("ALIAS--->", formValue["alias"])
			tournois.save()
			playerTournament(player=req.user, Tournament=tournois, name=formValue["alias"]).save()
		except Exception as e:
			try:
				tournois.numberOfPlayerNow = playerTournament.objects.filter(Tournament=tournois).count()
				tournois.save() 
				return JsonResponse({"error":e}, status=status.HTTP_200_OK)
			except Exception as e:
				return JsonResponse({"error": f"big error: {e}"}, status=status.HTTP_200_OK)
	return JsonResponse({"ok" : tournois.id}, status=status.HTTP_200_OK)
