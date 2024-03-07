from django.contrib import admin
from django.urls import path
from .views.chat import chat
from .views.home import home
import os

urlpatterns = [
	path('chat/', chat.say_hello),
	path('', home.home),
]
