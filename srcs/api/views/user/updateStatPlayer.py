from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match



def updateStat(player):
	data = []
	try:
		matchsOneWin = Match.objects.filter(uid_player_one=player, uid_winner=player)
		matchsTwoWin = Match.objects.filter(uid_player_two=player, uid_winner=player)
		matchsOneLoose = Match.objects.filter(uid_player_one=player).exclude(uid_winner=player).exclude(uid_winner=None)
		matchsTwoLoose = Match.objects.filter(uid_player_two=player).exclude(uid_winner=player).exclude(uid_winner=None)
		for match in matchsOneWin:
			data.append([{"date" : match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),"point":match.points_player_one,"win" : True}])
		for match in matchsTwoWin:
			data.append([{"date" : match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),"point":match.points_player_two,"win" : True}])
		for match in matchsOneLoose:
			data.append([{"date" : match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),"point":match.points_player_one,"win" : False}])
		for match in matchsTwoLoose:
			data.append([{"date" : match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),"point":match.points_player_two,"win" : False}])
		data = sorted(data, key=lambda x: x[0]['date'])
		elo = 0;
		point = 0
		player.victories = matchsOneWin.count() + matchsTwoWin.count()
		player.defeats = matchsOneLoose.count() + matchsTwoLoose.count()
		dataElo = []
		for match in data:
			if match[0]["win"] == False:
				elo -= 5
			if match[0]["win"] == True:
				elo += 5
			point += match[0]["point"] 
			elo += match[0]["point"]
			dataElo.append({match[0]["date"] : elo})
		player.elo = elo
		player.save()
		return JsonResponse({
			"win": player.victories,
			"loose": player.defeats,
			"point": point,
			"elo": elo
		}, status=200)
	except Exception as e:
		return JsonResponse({"error": str(e)}, status=500)


def updateStatPlayer(req, PongToken):
	try:
		playerInfo = Player.objects.filter(token_login=PongToken)
		if (playerInfo.count() != 1):
			raise Exception("Reload token")
		return updateStat(playerInfo[0])
	except Exception as e:
		return JsonResponse({"error": str(e)})