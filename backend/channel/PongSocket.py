from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from json.decoder import JSONDecodeError
from channels.layers import get_channel_layer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from time import sleep


import json
import asyncio
import time
import random

class Paddle:
	def __init__(self, side, canvas_width, canvas_height):
		if side == "right":
			self.x = canvas_width / 100
		else:
			self.x = canvas_width / 100 * 98
		self.point = 0
		self.w = canvas_width / 100
		self.h = canvas_height / 5
		self.y = (canvas_height / 2) - (self.h / 2)
		self.s = 10

	def up(self):
		if 0 < self.y:
			self.y -= self.s

	def down(self, canvas_height):
		if self.y + self.h < canvas_height:
			self.y += self.s

class Ball:
	def __init__(self, canvas_width, canvas_height):
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.init("")

	def init(self, side):
		self.x = self.canvas_width / 2
		self.y = self.canvas_height / 2
		self.r = 10
		rand_dir = round(random.random(), 2)
		rand_side = round(random.random(), 2)
		if rand_side < 0.5:
			self.vecX = 1
		else:
			self.vecX = -1
		if side == "right":
			self.vecX = 1
		if side == "left":
			self.vecX = -1
		if rand_dir < 0.5:
			self.vecY = (rand_dir - 1)
		else:
			self.vecY = rand_dir

	async def pointLoading(self, socket):
			await socket.send_message({"startGameIn": "3"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": "2"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": "1"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": ""})

	async def sendParticule(self, socket, color, side):
		await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : color, "side": side}})

	async def move(self, l_pad, r_pad, socket, match):
		if self.x + self.r >= r_pad.x and r_pad.y < self.y < r_pad.y + r_pad.h:
			await self.sendParticule(socket, "rPad", "right")
			self.vecX *= -1
		if self.x - self.r <= l_pad.x + l_pad.w and l_pad.y < self.y < l_pad.y + l_pad.h:
			await self.sendParticule(socket, "lPad", "left")
			self.vecX *= -1
		if self.y + self.r > self.canvas_height:
			await self.sendParticule(socket, "ball", "bottom")
			self.vecY *= -1
		if self.y - self.r < 0:
			await self.sendParticule(socket, "ball", "top")
			self.vecY *= -1
		if self.x - self.r < 0:
			r_pad.point += 1
			await self.sendParticule(socket, "ball", "left")
			await socket.send_message({"point": {"left": l_pad.point, "right": r_pad.point}})
			if (r_pad.point < 3 and l_pad.point < 3):
				await self.pointLoading(socket)
			self.init("right")
			return
		if self.x + self.r > self.canvas_width:
			l_pad.point += 1
			await self.sendParticule(socket, "ball", "right")
			await socket.send_message({"point": {"left": l_pad.point, "right": r_pad.point}})
			if (r_pad.point < 3 and l_pad.point < 3):
				await self.pointLoading(socket)
			self.init("left")
			return
		self.x += float(self.vecX) * self.s
		self.y += float(self.vecY) * self.s


class PongGame:
	def __init__(self, speed_paddle, speed_ball, canvas, socket, idPong, match):
		self.match = match
		self.idPong = idPong
		self.canvas = canvas
		self.socket = socket
		self.startGame = False
		self.playerNb = 0
		self.left_pad = Paddle("right", canvas["width"], canvas["height"])
		self.right_pad = Paddle("left", canvas["width"], canvas["height"])
		self.ball = Ball(canvas["width"], canvas["height"])
		self.right_pad.s = speed_paddle
		self.left_pad.s = speed_paddle
		self.ball.s = speed_ball
		self.Player1Down = False
		self.Player1Up = False
		self.Player2Down = False
		self.Player2Up = False
		self.Player1ready = False
		self.Player2ready = False
		self.startGameLoop = False

	async def sendData(self):
		data = {
			"game": {
				"lPad": {"x": self.left_pad.x, "y": self.left_pad.y},
				"rPad": {"x": self.right_pad.x, "y": self.right_pad.y},
				"ball": {"x": self.ball.x, "y": self.ball.y},
			}
		}
		await self.socket.send_message(data)


	def getMatch(self, uidMatch):
		from api.models.match import Match
		match =  Match.objects.get(uid=uidMatch)
		print("MATCH(getMatch)--->", match)
		return match

	async def game_loop(self):
		self.localGame = False
		self.startGameLoop = True
		match = await sync_to_async(self.getMatch)(self.socket.room_id)
		print("MATCH(game_loop)--->", match)
		startGameTime = round(time.time() * 1000)
		if self.match.local:
			pass
		elif not (self.match.tournament):
			while (self.Player1ready == False or self.Player2ready == False):
				nbOfPoint = int(((round(time.time() * 1000) - startGameTime) / 500)%4)
				await self.socket.send_message({"startGameIn": "Loading" + "." * nbOfPoint})
				if (startGameTime + 5000 < round(time.time() * 1000)):
					return await self.socket.send_message({"CancelMatch": ""})
				await asyncio.sleep(0.5)
		else:
			while (self.Player1ready == False or self.Player2ready == False):
				nbOfPoint = int(((round(time.time() * 1000) - startGameTime) / 1000)%4)
				await self.socket.send_message({"startGameIn": "Waiting player" + "." * nbOfPoint});
				if (self.match.tournament):
					await self.socket.send_message({"check": "connectionSetUp"})
				print("Player1Ready--->", self.Player1ready, "Player2Ready--->",self.Player2ready)
				await asyncio.sleep(0.5)

		await self.socket.send_message({"startGameIn": "Starting game !"})
		await self.match.startGame()
		if (self.match.local):
			await self.match.deleteGame()
			self.localGame = True
		await asyncio.sleep(2)
		await self.socket.send_message({"startGameIn": ""})
		await asyncio.sleep(1)
		await self.socket.send_message({"startGameIn": "3"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": "2"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": "1"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": "[START_GAME]"})
		while self.right_pad.point < 3 and self.left_pad.point < 3:
			print(self.socket.room_id)
			if (self.Player1Down):
				self.left_pad.down(self.canvas["height"])
			if (self.Player1Up):
				self.left_pad.up()
			if (self.Player2Down):
				self.right_pad.down(self.canvas["height"])
			if (self.Player2Up):
				self.right_pad.up()
			await self.ball.move(self.left_pad, self.right_pad, self.socket, self.match)
			await self.sendData()
			await asyncio.sleep(0.01)
		if (self.localGame):
			return
		await asyncio.sleep(1.00)
		if (self.left_pad.point == 3):
			winner = match.player1
			await match.endGame(self.left_pad.point, self.right_pad.point, match.player1)
		elif (self.right_pad.point == 3):
			winner = match.player2
			await match.endGame(self.left_pad.point, self.right_pad.point, match.player2)
		try:
			await self.socket.close()
		except (ConnectionResetError, BrokenPipeError, OSError) as e:
			print(f"Socket error: {e}")
		try:
			await self.socket.send(b'')  # Attempt to send a small packet
			print("socket was not closed")
		except (ConnectionResetError, BrokenPipeError, OSError) as e:
			print(f"Socket error: {e}")

		if winner:
			await self.notify_end_game(match, winner)
		return


	async def notify_end_game(self, match, winner):
		json_data = {}
		json_data["players"] = {}
		players = [match.player1, match.player2]
		for player in players:
			json_data["players"][str(player.id)] = player.username
			groupe_name = f'{player.id}'
			channel_layer = get_channel_layer()
			await (channel_layer.group_send)(
				groupe_name,
				{
					"type": "match_end",
					"message": f"Match ended with winner {winner}",
					"players": json_data["players"],
					"match_id": str(match.uid),
					"match_status": "FINISH",
					"is_tournament": match.tournament
				}
			)

async def getUser(self):
	from rest_framework_simplejwt.authentication import JWTAuthentication
	try:
		token_key = await getToken(self)
		jwt_authentication = JWTAuthentication()
		validated_token = jwt_authentication.get_validated_token(str(token_key))
		user = await sync_to_async(jwt_authentication.get_user)(validated_token)
		return user
	except Exception:
		return False

async def getToken(self):
	host = dict(self.scope['headers']).get(b'cookie', b'').decode('utf-8')
	pairs = host.split('; ')
	for pair in pairs:
		key, value = pair.split('=')
		if key.strip() == 'access':
			return value
	raise

class PongSocket(AsyncWebsocketConsumer):
	PongGameList = []
	async def connectionFail(self, message):
		await self.accept()
		self.room_group_name = "error"
		self.channel_name = "error"
		await self.channel_layer.group_add(self.room_group_name,self.channel_name)
		await self.send(text_data=json.dumps({"errorMessage":message}))
		await self.close()

	def matchMaking(self, user):
		from api.models.match import Match
		try:
			match = None
			matchs = Match.objects.all()
			for _match in matchs:
				print("_match")
				print(_match)
				if (_match.player1 != user and _match.status == "WAITPLAYERS" and not _match.tournament):
					match = _match
					print("match")
					print(match)
					break

			if match is None:
				print("GAMELAUNCH (player 1)")
				match = Match()
				match.player1 = user
				match.save()
				self.player = "1"
			else:
				print("GAMELAUNCH (player 2)")
				match.status = 'GAMELAUNCH'
				match.player2 = user
				match.save()
				self.player = "2"
			self.match = match
			return match
		except Exception as e:
			print(f"Exception {e}")
			return None

	def getMatch(self, uidMatch):
		from api.models.match import Match
		match = Match.objects.get(uid=uidMatch)
		if (match.player1 == self.user):
			self.player = "1"
		elif (match.player2 == self.user):
			self.player = "2"
		self.match = match
		return match

	async def connect(self):
		self.user = await getUser(self)
		if (self.user == False):
			return await self.connectionFail("Authentication failed")
		uidMatch = self.scope['url_route']['kwargs']['id']
		print(uidMatch)
		if (uidMatch == "null"):
			match = await sync_to_async(self.matchMaking)(self.user)
			if (match == None):
				return await self.connectionFail("Error with matchmaking")
		else:
			match = await sync_to_async(self.getMatch)(uidMatch)
			print(match.local)
			if (match.local):
				self.room_id = match.uid
				self.room_group_name = f'chat_{self.room_id}'
				await self.channel_layer.group_add(self.room_group_name,self.channel_name)
				await self.accept()
				await self.send(text_data=json.dumps({'PlayerNumber': "-1"}))
				await self.startGame(match)
				return
			elif (match.tournament and match.status != "WAITPLAYERS"):
				return await self.connectionFail("redirectTournament")


		self.room_id = match.uid
		self.room_group_name = f'chat_{self.room_id}'
		await self.channel_layer.group_add(self.room_group_name,self.channel_name)
		await self.accept()

		await self.send(text_data=json.dumps({'PlayerNumber': self.player}))
		if (match.tournament):
			instance = await self.getInstancePong()
			if (instance == None or instance.startGameLoop == False):
				await self.startGame(match)
		elif (self.player == "2"):
			await self.startGame(match)

	async def disconnect(self, close_code):
		instance = await self.getInstancePong()
		if (instance.localGame):
			return
		if (self.match.tournament):
			if(self.user == self.match.player1 and instance):
				instance.Player1ready = False
			elif(self.user == self.match.player2 and instance):
				instance.Player2ready = False
		await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
		await sync_to_async(self.match.refresh_from_db)()
		if (self.match.status == "WAITPLAYERS" and self.match.tournament == False):
			await sync_to_async(self.match.delete)()

	async def chat_message(self, event):
		await self.send(text_data=json.dumps(event['message']))

	async def send_message(self, message):
		await self.channel_layer.group_send(self.room_group_name,{"type": "chat_message","message": message})

	async def getInstancePong(self):
		for pong in self.PongGameList:
			if (self.room_id == pong.idPong):
				return pong
		return None

	async def receive(self, text_data):
		if text_data:
			try:
				jsondata = json.loads(text_data)
			except:
				print("Error in load message json")
				pass
			if (self.room_group_name == "error"):
				return
			elif ("check" in jsondata):
				if (jsondata["check"] == "connectionSetUpOK"):
					instance = await self.getInstancePong()
					if (self.player == "1" and instance != None):
						instance.Player1ready = True
					elif (self.player == "2" and instance != None):
						instance.Player2ready = True
			elif ("player" in jsondata):
				instance = await self.getInstancePong()
				if (jsondata["player"] == "1" and jsondata["key"] == "down" and jsondata["value"] == True): instance.Player1Down = True
				if (jsondata["player"] == "1" and jsondata["key"] == "down" and jsondata["value"] == False): instance.Player1Down = False
				if (jsondata["player"] == "1" and jsondata["key"] == "up" and jsondata["value"] == True): instance.Player1Up = True
				if (jsondata["player"] == "1" and jsondata["key"] == "up" and jsondata["value"] == False): instance.Player1Up = False
				if (jsondata["player"] == "2" and jsondata["key"] == "down" and jsondata["value"] == True): instance.Player2Down = True
				if (jsondata["player"] == "2" and jsondata["key"] == "down" and jsondata["value"] == False): instance.Player2Down = False
				if (jsondata["player"] == "2" and jsondata["key"] == "up" and jsondata["value"] == True): instance.Player2Up = True
				if (jsondata["player"] == "2" and jsondata["key"] == "up" and jsondata["value"] == False): instance.Player2Up = False
			else:
				print(f"text_data = {text_data}")
		else:
			print("Received empty message")


	async def startGame(self, match):
		global nbClient
		await self.send_message({"startGameIn": "Loading"})
		game = PongGame(5, 3, {"width": 800, "height": 600}, self, self.room_id, match)
		asyncio.create_task(game.game_loop())
		self.PongGameList.append(game)
		await self.send_message({"check": "connectionSetUp"})
