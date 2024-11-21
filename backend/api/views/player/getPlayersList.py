from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.playerModel import Player


@api_view(['GET'])
def PlayersList(request):
    queryset = Player.objects.all()
    return JsonResponse({'players': [player.username for player in queryset]}, status=status.HTTP_200_OK)