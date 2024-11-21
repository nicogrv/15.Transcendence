from api.models.tournament import Tournament
from api.models.playerTournament import playerTournament
from api.models.tournamentMatch import tournamentMatch
import random
from django.http import JsonResponse
from rest_framework import status



listMultiplePlayer = [2, 4, 8, 16, 32, 64]

def suite_aleatoire_ordre(x):
    nombres = list(range(x))
    random.shuffle(nombres)
    return nombres



def startTournament(id):
	playerInTournament = playerTournament.objects.filter(Tournament=id)
	if (playerInTournament.count() == 0):
		print("Warning in startTournament")
		return JsonResponse({"error" : "error"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	if not (playerInTournament.count() in listMultiplePlayer):
		return JsonResponse({"error" : f"error: number in game not good {playerInTournament.count()} ({listMultiplePlayer})"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	print("PlayersInTournament--->",playerInTournament.count())
	# print(not (playerInTournament.count() > 0 and playerInTournament.count() == playerInTournament[0].Tournament.numberOfPlayer))
	if not (playerInTournament.count() > 0 and playerInTournament.count() == playerInTournament[0].Tournament.numberOfPlayer):
		return
	if (playerInTournament[0].Tournament.status == 1 or playerInTournament[0].Tournament.status == 2):
		return
	# chef if 2 4 8 16 32
	# print(playerInTournament[0].Tournament.status == 0)
	playerInTournament[0].Tournament.def_INPROGRESS()
	suite = suite_aleatoire_ordre(playerInTournament.count())
	for index in range(int(len(suite)/2)):
		Tmatch = tournamentMatch()
		Tmatch.create(playerInTournament[0].Tournament, playerInTournament[int(index)*2].player, playerInTournament[int(index)*2+1].player, int(len(suite)/2), int(index+1), playerInTournament[0].Tournament.timeBetweenMatches)




		