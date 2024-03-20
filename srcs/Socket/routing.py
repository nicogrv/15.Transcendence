from django.urls import re_path
from .pong import Pong

websocket_urlpatterns = [
    re_path(r'match/(?P<match_id>[\w-]+)', Pong.as_asgi())
]