from django.contrib import admin
from django.urls import path
from .views.auth import authWithFortyTwo
from .views.auth import signUp
from .views.auth import signIn
from .views.user import getInfoPlayer
from .views.user import updateStatPlayer
from .views.pong import getIdMatch
from .views.user import getInfoPlayerOf
from .views.user import updateRelation


import os



urlpatterns = [
    path('auth/authWithFortyTwo', authWithFortyTwo.authWithFortyTwo),
    path('auth/signUp/', signUp.signUp),
    path('auth/signIn/', signIn.signIn),

    path('user/getInfoPlayer', getInfoPlayer.getInfoPlayer),
    path('user/getInfoPlayerOf/', getInfoPlayerOf.getInfoPlayerOf),
    path('user/updateRelation/', updateRelation.updateRelation),
    path('user/updateStatPlayer/<str:PongToken>', updateStatPlayer.updateStatPlayer),

    path('pong/getIdMatch/<str:UserToken>', getIdMatch.getIdMatch),
    
    
]
