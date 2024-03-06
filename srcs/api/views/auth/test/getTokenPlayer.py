from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import requests
import os

def getTokenPlayer(req):
	print("FETCH OK" + req)
	return JsonResponse({"json": req})