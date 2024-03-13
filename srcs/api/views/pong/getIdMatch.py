from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match

def findMatchToJoin(allMatch, player):
    i = 0;
    for match in allMatch:
        if (not match.uid_player_two) and (player.uid != match.uid_player_one.uid):
            return i
        i = i + 1;
    return -1;

def createNewMatch(player):
    print("new match")
    match = Match (
        uid_player_one=player,
        status=0,
    )
    match.save()
    data = []
    return {"uid": match.uid, "player": 1}

        
def joinMatch(match, player):
    match.uid_player_two = player
    match.status = 1
    match.save()
    data = {}
    return {"uid": match.uid, "player": 2}

def getIdMatch(req):
    if (req.COOKIES and "PongToken" in req.COOKIES):
	    players = Player.objects.filter(token_login=req.COOKIES["PongToken"])
    else:
        return JsonResponse({"error": "no cookie"})
    if (players.count() != 1):
        return JsonResponse({"error": "player != 1"})
    player = players[0]
    allMatch = Match.objects.filter()

    indexOfMatch = findMatchToJoin(allMatch, player)
    if (indexOfMatch == -1):
        data = createNewMatch(player)
    else:
        data = joinMatch(allMatch[indexOfMatch], player)
    return JsonResponse({"ok": data})