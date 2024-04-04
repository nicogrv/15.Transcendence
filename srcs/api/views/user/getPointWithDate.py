from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match
from datetime import datetime
import time

def getPointWithDate(req):
    player = ""
    data = []
    try:
        if (req.COOKIES and "PongToken" in req.COOKIES):
            playerInfo = Player.objects.filter(token_login=req.COOKIES["PongToken"])
            if (playerInfo.count() != 1):
                raise Exception("Reload token")
            player = playerInfo[0]
            matchsOne = Match.objects.filter(uid_player_one=player).exclude(uid_winner=None)
            matchsTwo = Match.objects.filter(uid_player_two=player).exclude(uid_winner=None)
        else:
            raise Exception("No cookie")
    except Exception as e:
        return JsonResponse({"error": str(e)})
    print(f"nb d elem: {matchsOne.count() + matchsTwo.count()}")
    for match in matchsOne:
        data.append({match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') : match.points_player_one})
    for match in matchsTwo:
        data.append({match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') : match.points_player_two})
    data = sorted(data, key=lambda x: list(x.keys())[0])
    return JsonResponse({"ok": data})