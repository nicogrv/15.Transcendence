from django.http import JsonResponse
from pong.models.player import Player
from pong.models.match import Match
from datetime import datetime
import time

def getPointWithDate(req):
    start_time = time.time()
    matchs = ""
    player = ""
    try:
        print(f"1 {(time.time() - start_time)*1000}")
        if (req.COOKIES and "PongToken" in req.COOKIES):
            playerInfo = Player.objects.filter(token_login=req.COOKIES["PongToken"])
            print(f"2 {(time.time() - start_time)*1000}")
            if (playerInfo.count() != 1):
                raise Exception("Reload token")
            print(f"3 {(time.time() - start_time)*1000}")
            player = playerInfo[0]
            matchs = Match.objects.all()
            print(f"4 {(time.time() - start_time)*1000}")
        else:
            return JsonResponse("No cookie")
    except Exception as e:
        return JsonResponse({"error": str(e)})
    data = []
    for match in matchs:
        if(match.uid_winner is not None):
            if (player == match.uid_player_one):
                data.append({match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') : match.points_player_one})
            elif (player == match.uid_player_two):
                data.append({match.ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ') : match.points_player_two})
    data = sorted(data, key=lambda x: list(x.keys())[0])
    print(f"5 {(time.time() - start_time)*1000}")
    return JsonResponse({"ok": data})