from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from pong.models import Player
import requests
import os
import json
import time


listKey = ['email', 'login', 'image', 'url']
# doc for keys -> https://api.intra.42.fr/apidoc/2.0/users/me.html


def getInfoOfStud(data):
	cleanData = {}
	url = "https://api.intra.42.fr/v2/me" 
	headers = {"Authorization": f"Bearer {data['access_token']}"}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		cleanData["token"] = data;
		for elem in list(response.json().keys()):
			if elem in listKey:
				cleanData[elem] = response.json()[elem];
		return cleanData
	else:
		return cleanData



def getTokenFortyTwo(code):
	client_id = os.environ['API_UID_KEY_FORTY_TWO']
	client_secret = os.environ['API_SECRET_KEY_FORTY_TWO']
	server_ip = os.environ['SERVER_IP']
	server_port = os.environ['SERVER_PORT']
	server_protocol = os.environ['SERVER_PROTOCOL']
	redirect_uri_forty_two = os.environ['REDIRECT_URI_FORTY_TWO']
	redirect_uri = f"{server_protocol}://{server_ip}:{server_port}{redirect_uri_forty_two}"
	try:
		url = "https://api.intra.42.fr/oauth/token"
		data = {
			'grant_type': 'authorization_code',
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code,
			'redirect_uri': redirect_uri
		}
		response = requests.post(url, data=data)
		data = response.json()
		if ("access_token" in data):
			data = getInfoOfStud(data)
			return (data)
		return ({"error": data})
	except Exception as e:
		return ({"error": e})


def addPlayerInDb(data):
	newPlayer = Player(
		username=data['login'],
		login_42=data['login'],
		pic=data['image']['link'],
		email=data['email']
	)
	token = newPlayer.update_token();
	newPlayer.save()
	return token;

def checkIfPlayerOnDb(data):
	print(data)
	dbResult = Player.objects.filter(login_42=data["login"])
	if (dbResult.count() == 0):
		return False
	elif (dbResult.count() == 1):
		return True
	else:
		data = {"error": "dbResult.count() != 0 || 1"}

def authWithFortyTwo(req):
	data = getTokenFortyTwo(req.GET.get('code'))
	if ("error" in data): return JsonResponse(data)
	PlayerOnDb = checkIfPlayerOnDb(data)
	if ("error" in data): return JsonResponse(data)
	if (PlayerOnDb == False):
		response = JsonResponse(data)
		response.set_cookie('PongToker', addPlayerInDb(data), max_age=3600)
		return response;
	return JsonResponse(data)






# uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
# username = models.SlugField(max_length=24, unique=True)
# login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)
# pic = models.TextField(null=True, blank=True)
# email = models.EmailField(null=True, blank=True)
# elo = models.IntegerField(default=0)
# victories = models.IntegerField(default=0)
# defeats = models.IntegerField(default=0)
# status = models.IntegerField(choices=Status.choices, default=Status.OFFLINE)

# token_login = models.UUIDField(null=True, blank=True, unique=True)
# token_login_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
# token_login_end_at = models.DateTimeField(null=True, blank=True)

# created_at = models.DateTimeField(auto_now_add=True)
# updated_at = models.DateTimeField(auto_now=True)