from django.http import JsonResponse
from pong.models.player import Player


def getInfoPlayer(req):
    data = {}
    if (req.COOKIES and "PongToken" in req.COOKIES):
        token = req.COOKIES["PongToken"]
    else:
        return JsonResponse({"error": "No cookie"})
    try:
        playerInfo = Player.objects.filter(token_login=token)
    except Exception as e:
        return JsonResponse({"error": str(e)})
        
    if (playerInfo.count() != 1):
        return JsonResponse({"error": "error"})
    data['username'] = playerInfo[0].getUsername()
    data['pic'] = playerInfo[0].getPic()
    data['elo'] = playerInfo[0].getElo()
    data['victories'] = playerInfo[0].getVictories()
    data['defeats'] = playerInfo[0].getDefeats()
    data['status'] = playerInfo[0].getStatus()
    data['token_login'] = playerInfo[0].getToken_login()
    data['token_login_created_at'] = playerInfo[0].getToken_login_created_at()
    data['token_login_end_at'] = playerInfo[0].getToken_login_end_at()
    data['created_at'] = playerInfo[0].getCreated_at()
    data['updated_at'] = playerInfo[0].getUpdated_at()
    return JsonResponse(data)
