from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import requests
import os
import json
listKey = ['email', 'login', 'image', 'url']
# foc for keys -> https://api.intra.42.fr/apidoc/2.0/users/me.html


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


def getTokenFortyTwo(req):
	client_id = os.environ['API_UID_KEY']
	client_secret = os.environ['API_SECRET_KEY']
	server_ip = os.environ['SERVER_IP']
	server_port = os.environ['SERVER_PORT']
	server_protocol = os.environ['SERVER_PROTOCOL']
	code = req.GET.get('code')
	redirect_uri = f"{server_protocol}://{server_ip}:{server_port}/api/auth/getTokenFortyTwo"
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
			return JsonResponse(data)
		return JsonResponse({"error": data})
	except Exception as e:
		return JsonResponse({"error": e})

