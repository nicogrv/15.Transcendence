from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channel.routing import websocket_urlpatterns as pongsocket_urlpatterns
from api.routing import websocket_urlpatterns as notifysocket_urlpatterns
import os

os.environ.setdefault('DJANGO_SETTING_MODULE', 'backend.settings')

django_app = get_asgi_application() # ajouter ca pour gerer simple http requests

combined_urlpatterns = pongsocket_urlpatterns + notifysocket_urlpatterns

application = ProtocolTypeRouter({
    'http': AuthMiddlewareStack(django_app),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(combined_urlpatterns)
        )
	),
})
