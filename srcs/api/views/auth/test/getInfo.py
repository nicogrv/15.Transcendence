from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import requests
import os

	

def getTokenAuthFourtyTwo():
	



def getInfo(req):
	client_id = os.environ['API_UID_KEY']
	client_secret = os.environ['API_SECRET_KEY']
	code = req.GET.get('code')
	try:
		url = "https://api.intra.42.fr/oauth/token"
		data = {
			'grant_type': 'authorization_code',
			'client_id': 'u-s4t2ud-9198daa6a4877961ff5b7a3ca58e5990fd4f618ddc61420e8aa18e18ed316472',
			'client_secret': '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',
			'code': code,
			'redirect_uri': 'http://127.0.0.1:8000/api/auth/test'
		}
		response = requests.post(url, data=data)
		data = response.json()
		if ("access_token" in data):
			return JsonResponse(data)
	except Exception as e:
		return HttpResponse(e)