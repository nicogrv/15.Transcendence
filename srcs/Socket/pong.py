from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Test(AsyncWebsocketConsumer):
	async def connect(self):
		print("CONNECT")
		await self.accept()

	async def disconnect(self, close_code):
		print("DISCONNECT")
		pass

	async def receive(self, text_data):
		if text_data:
			print(text_data)
		else:
			# Handle empty message
			print("Received empty message")