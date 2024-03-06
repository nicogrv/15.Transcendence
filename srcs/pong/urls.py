from django.contrib import admin
from django.urls import path
from .views.chat import chat
import os

urlpatterns = [
	path('chat/', chat.say_hello)
]
