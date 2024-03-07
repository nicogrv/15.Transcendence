from django.shortcuts import render
from django.http import HttpResponse

# def send_message():

# Create your views here.
def home(request):
	return render(request, 'index.html')