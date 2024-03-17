from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import requests
import os

def getInfo(req):
	client_id = os.environ['API_UID_KEY']
	client_secret = os.environ['API_SECRET_KEY']
	code = req.GET.get('code')
	try:
		url = "https://api.intra.42.fr/oauth/token"
		data = {
			'grant_type': 'authorization_code',
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code,
			'redirect_uri': 'http://127.0.0.1:8000/'
		}
		response = requests.post(url, data=data)
		data = response.json()
		if ("access_token" in data):
			return JsonResponse(data)
	except Exception as e:
		return HttpResponse(e)