from django.urls import re_path

from .pong import Pong

websocket_urlpatterns = [
    re_path(r'match', Pong.as_asgi()),
]