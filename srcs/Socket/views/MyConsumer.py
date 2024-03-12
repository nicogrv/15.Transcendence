from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Logique de connexion
        pass

    async def disconnect(self, close_code):
        # Logique de déconnexion
        pass

    async def receive(self, text_data):
        # Logique de réception de message
        pass