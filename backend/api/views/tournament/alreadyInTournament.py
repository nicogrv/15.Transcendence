
from django.http import JsonResponse
from api.serializers.profileSerializer import ProfileSerializer
from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
import json



@api_view(['GET'])
def alreadyInTournament(req):
	userInTournament = playerTournament.objects.filter(player=req.user)
	for user in userInTournament:
		if (user.Tournament.status != 2):
			return JsonResponse({"tournament" :user.Tournament.id}, status=status.HTTP_200_OK)
	return JsonResponse({"tournament" : "no"}, status=status.HTTP_200_OK)
