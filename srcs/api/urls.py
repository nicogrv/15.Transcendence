from django.contrib import admin
from django.urls import path
from .views.auth import getTokenFortyTwo
import os



urlpatterns = [
    path('auth/getTokenFortyTwo', getTokenFortyTwo.getTokenFortyTwo),
]
