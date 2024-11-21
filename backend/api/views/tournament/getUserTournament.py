from django.http import JsonResponse
from api.serializers.profileSerializer import ProfileSerializer
from api.models.playerTournament import playerTournament
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
import json


@api_view(['GET'])
def getUserTournament(req):
	listTournament = []
	filterTournament = playerTournament.objects.filter(player=req.user)
	for tmp in filterTournament:
		elem = tmp.Tournament.json()
		elem["alias"] = tmp.name
		listTournament.append(elem)
	return JsonResponse({"ok" : listTournament}, status=status.HTTP_200_OK)