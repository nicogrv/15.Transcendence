from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match

def getEloWithDate(req):
    player = ""
    data = []
    try:
        if (req.COOKIES and "PongToken" in req.COOKIES):
            playerInfo = Player.objects.filter(token_login=req.COOKIES["PongToken"])
            if (playerInfo.count() != 1):
                raise Exception("Reload token")
            player = playerInfo[0]
            matchsOneWin = Match.objects.filter(uid_player_one=player, uid_winner=player)
            matchsTwoWin = Match.objects.filter(uid_player_two=player, uid_winner=player)
            matchsOneLoose = Match.objects.filter(uid_player_one=player).exclude(uid_winner=player).exclude(uid_winner=None)
            matchsTwoLoose = Match.objects.filter(uid_player_two=player).exclude(uid_winner=player).exclude(uid_winner=None)
        else:
            raise Exception("No cookie")
    except Exception as e:
        return JsonResponse({"error": str(e)})
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
    dataElo = []
    for match in data:
        if match[0]["win"] == False:
            elo -= 5
        if match[0]["win"] == True:
            elo += 5
        elo += match[0]["point"]
        dataElo.append({match[0]["date"] : elo})

    return JsonResponse({"ok": dataElo},status=200, json_dumps_params={'indent': 2})