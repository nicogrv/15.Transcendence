from rest_framework.response import Response
from api.models.playerModel import Player
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import models
from rest_framework_simplejwt import tokens
from rest_framework import status

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

def cookie_tokens(request, user):
    tokens = get_user_tokens(user)
    res = Response()
    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=tokens["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )

    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        value=tokens["refresh"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    res.data = tokens
    res["X-CSRFToken"] = csrf.get_token(request)
    models.update_last_login(None, user)
    user.status_profile = Player.STATUS.ONLINE
    user.save(update_fields=['status_profile'])
    return res