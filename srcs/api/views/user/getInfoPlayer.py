from django.http import JsonResponse
from pong.models.player import Player

def getInfoPlayer(req, token):
    data = {}
    playerInfo = Player.objects.filter(token_login=token)
    data['username'] = playerInfo[0].getUsername()
    data['pic'] = playerInfo[0].getPic()
    data['elo'] = playerInfo[0].getElo()
    data['defeats'] = playerInfo[0].getDefeats()
    data['status'] = playerInfo[0].getStatus()
    data['token_login'] = playerInfo[0].getToken_login()
    data['token_login_created_at'] = playerInfo[0].getToken_login_created_at()
    data['token_login_end_at'] = playerInfo[0].getToken_login_end_at()
    data['created_at'] = playerInfo[0].getCreated_at()
    data['updated_at'] = playerInfo[0].getUpdated_at()
    return JsonResponse(data)
