import json
from channels.generic.websocket import WebsocketConsumer
from pong.models.player import Player
from django.db.models.functions import Length

class SocketSession(WebsocketConsumer):
	def connect(self):
		self.accept()
		self.player = None
		self.uidPlayer = self.scope['url_route']['kwargs']['tokenLogin']
		print(self.uidPlayer)
		try:
			self.player = Player.objects.get(token_login=self.uidPlayer)
			print(self.player)
			self.player.status = 1
			self.player.save()
		except Exception as e:
			print(f"error socket session: {e}")
			pass

	def disconnect(self, close_code):
		if self.player is not None:
			self.player.status = 0
			self.player.save()
		pass

	def receive(self, text_data):
		if (text_data):
			jsondata = json.loads(text_data)
			print(jsondata)
			self.send(text_data=json.dumps({"message": jsondata}))
		
		if "searchFriends" in jsondata:
			self.searchFriends(jsondata["searchFriends"])


	def	searchFriends(self, value):
		data = []
		players = Player.objects.filter(username__icontains=value).annotate(
			lenUsername=Length('username')
		).order_by('lenUsername')
		for player in players:
			data.append(player.getUsername())
			print(player.getUsername())
		print(f"value: {value}")
		self.send(text_data=json.dumps({"usernameSearchValue": data}))
