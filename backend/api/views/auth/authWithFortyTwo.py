from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils.crypto import get_random_string
from api.models.playerModel import Player
from api.views.auth.signUp import signUp
from api import tokenTools
from api.serializers.loginSerializer import LoginFortyTwoSerializer
from api.models.twoFactorAuthentication import TwoFactorAuthentication
import requests
from api.models.twoFactorAuthentication import TwoFactorAuthentication
import os


# doc for keys -> https://api.intra.42.fr/apidoc/2.0/users/me.html
timeout = 5


@api_view(['POST', 'GET'])
@authentication_classes([]) # for allowing unauthenticated users
@permission_classes([AllowAny]) # for allowing unauthenticated users
def authWithFortyTwo(request):
    if ("uid" in request.data and "tfaCode" in request.data):
        tmp = TwoFactorAuthentication.objects.get(uid=request.data["uid"])
        if (tmp.checkCode(request.data["tfaCode"])):
            return tokenTools.cookie_tokens(request, tmp.player)
        return JsonResponse({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


    data = getTokenFortyTwo(request.GET.get('code'))
    if data is None:
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    player_exists = Player.objects.filter(username=data['username'])
    check = Player.objects.filter(email=data['email'])
    if player_exists and check:
        newPlayer = Player.objects.get(email=data['email'])
        serializer = LoginFortyTwoSerializer(data={'username': data['username'], 'password': newPlayer.password})
        if (newPlayer.tfaActive and not "uid" in request.data):
            tmp = TwoFactorAuthentication(player=newPlayer)
            tmp.save()
            return JsonResponse({'tfa': tmp.uid})
        if serializer.is_valid():
            return tokenTools.cookie_tokens(request, newPlayer)
        else:
            return JsonResponse({'message': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
    elif player_exists:
        return JsonResponse({'message': 'Player already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        generated_password = get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password': generated_password,
            'confirm_password': generated_password,
            'avatar': data['avatar'],
            'is_42_user': True
        }

        client = APIClient() # simulate the signup process to avoid making a http request
        signup_response = client.post('/api/signUp', user_data, format='json')

        # signup_response = requests.post('http://localhost:8000/api/signUp', data=user_data) # the old version with endpoint call
        if signup_response.status_code == 200:
            tokens = signup_response.json()
            res = JsonResponse(tokens)
            return res
        else:
            return JsonResponse({'message': 'Signup failed'}, status=status.HTTP_400_BAD_REQUEST)


def getTokenFortyTwo(code):
    client_id = os.environ['API_UID_KEY_FORTY_TWO']
    client_secret = os.environ['API_SECRET_KEY_FORTY_TWO']
    server_ip = os.environ['SERVER_IP']
    server_port = os.environ['SERVER_PORT']
    server_protocol = os.environ['SERVER_PROTOCOL']
    redirect_uri_forty_two = os.environ['REDIRECT_URI_FORTY_TWO']
    redirect_uri = f"{server_protocol}://{server_ip}:{server_port}{redirect_uri_forty_two}"

    try:
        url = "https://api.intra.42.fr/v2/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        response = requests.post(url, data=data, timeout=timeout)

        if response.status_code != 200:
            return JsonResponse({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        data = response.json()
        if ("access_token" in data):
            data = getInfoOfStud(data)
            return data
    except Exception as e:
        return ({"error": str(e)})


def getInfoOfStud(data):
    url = "https://api.intra.42.fr/v2/me"
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = requests.get(url, headers=headers, timeout=timeout)

    if response.status_code == 200:
        parsed_data = response.json()
        image_info = parsed_data.get('image')
        email = parsed_data.get('email')
        avatar = image_info['versions']['small']
        username = parsed_data.get('login')
        return {
            'username': username,
            'email': email,
            'avatar': avatar
        }
    else:
        return JsonResponse({'message': 'Failed to fetch user information'}, status=status.HTTP_400_BAD_REQUEST)
