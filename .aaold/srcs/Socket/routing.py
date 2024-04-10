from django.urls import re_path
from .pong import Pong
from .socketSession import SocketSession


websocket_urlpatterns = [
    re_path(r'match/(?P<uidUser>[\w-]+)', Pong.as_asgi()),
    re_path(r'socketSession/(?P<tokenLogin>[\w-]+)', SocketSession.as_asgi()),
]