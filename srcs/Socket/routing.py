from django.urls import re_path
from .pong import Pong

websocket_urlpatterns = [
    re_path(r'match/(?P<uidUser>[\w-]+)', Pong.as_asgi())
]