from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class Pong(AsyncWebsocketConsumer):
	clients = set()
	async def connect(self):
		print("CONNECT")
		await self.accept()
		Pong.clients.add(self)
		if len(self.clients) == 2:
			await self.startGame()

	async def disconnect(self, close_code):
		print("DISCONNECT")
		Pong.clients.remove(self)
		pass

	async def receive(self, text_data):
		if text_data:
			jsondata = json.loads(text_data)
			print(jsondata)
		else:
			print("Received empty message")

	async def send_to_all_clients(self, data):
		for client in Pong.clients:
			await client.send(json.dumps(data))
	async def startGame(self):
		await sync_to_async(self.run_game)()
	def run_game(self):
		print("Starting pong game...")
				
