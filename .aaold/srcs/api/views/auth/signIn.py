from pong.models.player import Player
from django.http import JsonResponse
from django.db import IntegrityError

def signIn(req):
    username = req.GET.get('username')
    password = req.GET.get('password')
    response = JsonResponse({"ok" : "Player Sign In"})
    playerUsername = Player.objects.filter(username=username)
    playerEmail = Player.objects.filter(email=username)
    if (playerUsername.count() == 0 and playerEmail.count() == 0):
        return JsonResponse({"error" : "There is no player with this username or email address"})
    if (playerUsername.count() == 1 and playerUsername[0].checkPassword(password)):
        token, startToken, endToken = playerUsername[0].update_token()
        response.set_cookie('PongToken', token, max_age=endToken - startToken) # check max age
    elif (playerEmail.count() == 1 and playerEmail[0].checkPassword(password)):
        token, startToken, endToken = playerEmail[0].update_token()
        response.set_cookie('PongToken', token, max_age=endToken - startToken) # check max age
    else:
        return JsonResponse({"error" : str("Error in signIn.py file" + str(playerEmail.count()) + "-" + str(playerUsername.count()))})
    return response
