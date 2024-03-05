from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request, name):
    return render(request, 'base.html', {'name' : name})