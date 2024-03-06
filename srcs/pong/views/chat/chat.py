from django.shortcuts import render
from django.http import HttpResponse

# def send_message():

# Create your views here.
def say_hello(request):
	return render(request, 'chat.html')