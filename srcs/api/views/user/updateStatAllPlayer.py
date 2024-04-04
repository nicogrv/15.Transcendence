from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match
from api.views.user.updateStatPlayer import updateStat



def updateStatAllPlayer(req):
	returnValue = 0
	try:
		playerInfo = Player.objects.all()
		for player in playerInfo:
			returnValue = updateStat(player)
			print(returnValue)
			if (returnValue.status_code == 500):
				return returnValue
	except Exception as e:
		return JsonResponse({"error": str(e)})
	return JsonResponse({"ok" : "All player update"})
