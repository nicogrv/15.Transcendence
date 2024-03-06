from django.contrib import admin
from django.urls import path
from .views.auth.test import getInfo
from .views.auth.test import getTokenPlayer
import os



urlpatterns = [
    path('auth/test', getInfo.getInfo),
    path('auth/getTokenPlayer', getTokenPlayer.getTokenPlayer),
    # path('', admin.site.urls),
]
