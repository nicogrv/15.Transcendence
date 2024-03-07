from django.contrib import admin
from django.urls import path
from .views.auth import authWithFortyTwo
from .views.user import getInfoPlayer
import os



urlpatterns = [
    path('auth/authWithFortyTwo', authWithFortyTwo.authWithFortyTwo),
    path('user/getInfoPlayer/<str:token>', getInfoPlayer.getInfoPlayer),
]
