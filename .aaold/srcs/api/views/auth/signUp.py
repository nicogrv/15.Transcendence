from pong.models.player import Player
from django.http import JsonResponse
from django.db import IntegrityError

def signUp(req):
    username = req.GET.get('username')
    email = req.GET.get('email')
    password = req.GET.get('password')
    response = JsonResponse({"ok" : "Player Sign up"})
    try :
        newPlayer = Player(username=username, email=email)
        if (newPlayer.isValidPassword(password) != ""):
            return JsonResponse({"error" : newPlayer.isValidPassword(password)})
        else:
            newPlayer.setPassword(password)
            newPlayer.save()
            token, startToken, endToken = newPlayer.update_token()
            response.set_cookie('PongToken', token, max_age=endToken - startToken) # check max age
    except IntegrityError as e:
        if ('DETAIL:  Key (username)' in str(e)):
            return JsonResponse({"error" : "Username already use"})
        return JsonResponse({"error" : str(e)})
    return response


