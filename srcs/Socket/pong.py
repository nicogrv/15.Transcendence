from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


import math
import random
import time
import asyncio	


global Player1Up
global Player1Down
global Player2Up
global Player2Down
global nextFrame

nextFrame = False
Player1Up = False
Player1Down = False
Player2Up = False
Player2Down = False

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

	async def move(self, l_pad, r_pad):
		if self.x + self.r >= r_pad.x and r_pad.y < self.y < r_pad.y + r_pad.h:
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "rPad"}})
			self.vecX *= -1
		if self.x - self.r <= l_pad.x + l_pad.w and l_pad.y < self.y < l_pad.y + l_pad.h:
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "lPad"}})
			self.vecX *= -1
		if self.y + self.r > self.canvas_height:
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "ball"}})
			self.vecY *= -1
		if self.y - self.r < 0:
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "ball"}})
			self.vecY *= -1
		if self.x - self.r < 0:
			r_pad.point += 1
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "ball"}})
			await self.socket.send_to_all_clients({"point": {"left": l_pad.point, "right": l_pad.point}})
			self.init("right")
			return
		if self.x + self.r > self.canvas_width:
			l_pad.point += 1
			await self.socket.send_to_all_clients({"particle": {"x": self.x, "y": self.y, "color" : "ball"}})
			await self.socket.send_to_all_clients({"point": {"left": l_pad.point, "right": l_pad.point}})
			self.init("left")
			return
		self.x += float(self.vecX)
		self.y += float(self.vecY)


class PongGame:
	def __init__(self, speed_paddle, speed_ball, canvas, socket):
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

	async def sendData(self):
		data = {
			"game": {
				"lPad": {"x": self.left_pad.x, "y": self.left_pad.y},
				"rPad": {"x": self.right_pad.x, "y": self.right_pad.y},
				"ball": {"x": self.ball.x, "y": self.ball.y},
			}
		}
		await self.socket.send_to_all_clients(data)

	async def game_loop(self):
		frame = 0
		global Player1Up
		global Player1Down
		global Player2Up
		global Player2Down
		global nextFrame
		while True:
			# print(Player1Down, Player1Up, Player2Down, Player2Up)
			if (Player1Down):
				self.right_pad.down(self.canvas["height"])
			if (Player1Up):
				self.right_pad.up()
			if (Player2Down):
				self.left_pad.down(self.canvas["height"])
			if (Player2Up):
				self.left_pad.up()
			if (nextFrame):
				# nextFrame = False	
				self.ball.move(self.left_pad, self.right_pad)
			await self.sendData()
			await asyncio.sleep(0.001)
			frame += 1

class Pong(AsyncWebsocketConsumer):
	clients = set()

	async def connect(self):
		print("CONNECT")
		await self.accept()
		Pong.clients.add(self)
		print("Nb clien:", len(self.clients))
		await self.send(text_data=json.dumps({"message": "Hello client"}))
		if len(self.clients) == 2:
			await self.startGame()

	async def disconnect(self, close_code):
		print("DISCONNECT")
		Pong.clients.remove(self)

	async def receive(self, text_data):
		print("text_data")
		if text_data:
			jsondata = json.loads(text_data)
			global Player1Up
			global Player1Down
			global Player2Up
			global Player2Down
			global nextFrame
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "down" and jsondata["value"] == True):
				Player1Down = True
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "down" and jsondata["value"] == False):
				Player1Down = False
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "up" and jsondata["value"] == True):
				Player1Up = True
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "up" and jsondata["value"] == False):
				Player1Up = False
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "down" and jsondata["value"] == True):
				Player2Down = True
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "down" and jsondata["value"] == False):
				Player2Down = False
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "up" and jsondata["value"] == True):
				Player2Up = True
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "up" and jsondata["value"] == False):
				Player2Up = False
			print(jsondata)
			if ("nextFrame" in jsondata):
				print("coucou")
				nextFrame = True
		else:
			print("Received empty message")

	async def send_to_all_clients(self, data):
		for client in Pong.clients:
			await client.send(json.dumps(data))

	async def startGame(self):
			
		print("Starting pong game...")
		await asyncio.sleep(0.3)
		await self.send_to_all_clients({"startGameIn": "3"})
		await asyncio.sleep(0.3)
		await self.send_to_all_clients({"startGameIn": "2"})
		await asyncio.sleep(0.3)
		await self.send_to_all_clients({"startGameIn": "1"})
		await asyncio.sleep(0.3)
		await self.send_to_all_clients({"startGameIn": ""})

		canvas = {"width": 800, "height": 600}
		pongGame = PongGame(5, 1, canvas, self)
		asyncio.create_task(pongGame.game_loop())
		print("End pong game")