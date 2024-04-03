from django.http import JsonResponse
from pong.models.player import Player


def getRanking(req):
    data = []
    try:
        if (req.COOKIES and "PongToken" in req.COOKIES):
            if (Player.objects.filter(token_login=req.COOKIES["PongToken"]).count() != 1):
                raise Exception("Session not good, please retry with good session")
            elements_tries = Player.objects.all().order_by('-elo')
            for element in elements_tries:
                data.append({element.username: element.elo})    
        else:
            raise Exception("No cookie")
    except Exception as e:
        return JsonResponse({"error": str(e)})
    return JsonResponse({"ok": data})