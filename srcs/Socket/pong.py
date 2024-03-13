from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Test(AsyncWebsocketConsumer):
	clients = set()
	async def connect(self):
		print("CONNECT")
		await self.accept()
		Test.clients.add(self)

	async def disconnect(self, close_code):
		print("DISCONNECT")
		Test.clients.remove(self)
		pass

	async def receive(self, text_data):
		if text_data:
			jsondata = json.loads(text_data)
			# print(str(jsondata['ball']['x']) + " " + str(jsondata['ball']['y']) + " " + str(jsondata['lPad']['x']) + " " + str(jsondata['lPad']['y']))
			await self.send_to_all_clients(jsondata)
		else:
			print("Received empty message")

	async def send_to_all_clients(self, data):
		for client in Test.clients:
			await client.send(json.dumps(data))