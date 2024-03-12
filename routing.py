from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .Socket.views.MyConsumer import MyConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/some_endpoint/', MyConsumer.as_asgi()),
        ])
    ),
})
