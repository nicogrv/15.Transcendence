from django.contrib import admin
from django.urls import path
from .views.auth import authWithFortyTwo
import os



urlpatterns = [
    path('auth/authWithFortyTwo', authWithFortyTwo.authWithFortyTwo),
]
