from django.http import JsonResponse
from pong.models.player import Player
def test(req):
    print(req.GET.get('message'))
    return JsonResponse({"ok": req.GET.get('message')})