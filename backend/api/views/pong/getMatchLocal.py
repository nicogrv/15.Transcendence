
from django.http import JsonResponse
from api.serializers.profileSerializer import ProfileSerializer

from api.models.playerModel import Player
from api.models.match import Match
from rest_framework import status
from rest_framework.decorators import api_view
import json



@api_view(['GET'])
def getMatchLocal(req):
	_match = Match(player1=req.user, player2=req.user, local=True)
	_match.save()
	return JsonResponse({"uid" : _match.uid}, status=status.HTTP_200_OK)
