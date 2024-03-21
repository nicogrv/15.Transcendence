from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match

def updateStatPlayer(req, PongToken):
	playersCheck = Player.objects.filter(token_login=PongToken)
	if (playersCheck.count() != 1):
		print("ERROR")
		return JsonResponse({"error" : f" multi / no, players with token: {PongToken}"})
	player = playersCheck[0]
	Matchs = Match.objects.all()
	win = 0
	loose = 0
	point = 0
	for match in Matchs:
		if (match.uid_player_one == player and match.uid_player_two is not None):
			point += match.points_player_one
			if (match.uid_winner == player):
				win += 1
			else:
				loose += 1
		elif (match.uid_player_two == player and match.uid_player_one is not None):
			point += match.points_player_two
			if (match.uid_winner == player):
				win += 1
			else:
				loose += 1

	player.victories = win
	player.defeats = loose
	elo = ((win * 5) + point) - (loose * 5)
	if (elo < 0):
		player.elo = 0
	else:
		player.elo = elo
	player.save()
	return JsonResponse({
        "win": win,
        "loose": loose,
        "point": point,
        "elo": elo
    })
