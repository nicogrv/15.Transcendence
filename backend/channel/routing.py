from django.urls import re_path
from channel.PongSocket import PongSocket


websocket_urlpatterns = [
    re_path(r'pongSocket/(?P<id>[\w-]+)', PongSocket.as_asgi()),
]