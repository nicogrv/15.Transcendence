from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pong.models.match import Match


import math
import random
import time
import asyncio	


global Player1Up
global Player1Down
global Player2Up
global Player2Down

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

	async def pointLoading(self, socket):
			await socket.send_message({"startGameIn": "3"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": "2"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": "1"})
			await asyncio.sleep(0.42)
			await socket.send_message({"startGameIn": ""})


	async def move(self, l_pad, r_pad, socket):
		if self.x + self.r >= r_pad.x and r_pad.y < self.y < r_pad.y + r_pad.h:
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "lPad", "side": "right"}})
			self.vecX *= -1
		if self.x - self.r <= l_pad.x + l_pad.w and l_pad.y < self.y < l_pad.y + l_pad.h:
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "rPad", "side": "left"}})
			self.vecX *= -1
		if self.y + self.r > self.canvas_height:
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "ball", "side": "bottom"}})
			self.vecY *= -1
		if self.y - self.r < 0:
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "ball", "side": "top"}})
			self.vecY *= -1
		if self.x - self.r < 0:
			r_pad.point += 1
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "ball", "side": "left"}})
			await socket.send_message({"point": {"left": l_pad.point, "right": r_pad.point}})
			if (r_pad.point < 2 and l_pad.point < 2):
				await self.pointLoading(socket)
			self.init("right")
			return
		if self.x + self.r > self.canvas_width:
			l_pad.point += 1
			await socket.send_message({"particle": {"x": self.x, "y": self.y, "color" : "ball", "side": "right"}})
			await socket.send_message({"point": {"left": l_pad.point, "right": r_pad.point}})
			if (r_pad.point < 2 and l_pad.point < 2):
				await self.pointLoading(socket)
			self.init("left")
			return
		self.x += float(self.vecX) * self.s
		self.y += float(self.vecY) * self.s


class PongGame:
	def __init__(self, speed_paddle, speed_ball, canvas, socket, idPong):
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
		self.test = 0
		self.Player1Down = False
		self.Player1Up = False
		self.Player2Down = False
		self.Player2Up = False

	async def sendData(self):
		data = {
			"game": {
				"lPad": {"x": self.left_pad.x, "y": self.left_pad.y},
				"rPad": {"x": self.right_pad.x, "y": self.right_pad.y},
				"ball": {"x": self.ball.x, "y": self.ball.y},
			}
		}
		await self.socket.send_message(data)

	async def game_loop(self):
		frame = 0
		global Player1Up
		global Player1Down
		global Player2Up
		global Player2Down

		await self.socket.send_message({"startGameIn": "3"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": "2"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": "1"})
		await asyncio.sleep(0.7)
		await self.socket.send_message({"startGameIn": ""})
		while True and self.right_pad.point < 3 and self.left_pad.point < 3:
			if (self.Player1Down):
				self.right_pad.down(self.canvas["height"])
			if (self.Player1Up):
				self.right_pad.up()
			if (self.Player2Down):
				self.left_pad.down(self.canvas["height"])
			if (self.Player2Up):
				self.left_pad.up()
			await self.ball.move(self.left_pad, self.right_pad, self.socket)
			await self.sendData()
			await asyncio.sleep(0.01)
			frame += 1
		return

global nbClient
nbClient = []

import datetime

class Pong(AsyncWebsocketConsumer):
	PongGameList = []

	async def connect(self):
		global nbClient

		match_id = self.scope['url_route']['kwargs']['match_id']
		self.room_id = match_id
		self.room_group_name = f'chat_{self.room_id}'
		await self.channel_layer.group_add(self.room_group_name,self.channel_name)
		found = False
		for item in nbClient:
			if match_id in item:
				item[match_id] += 1
				found = True
				await self.accept()
				if (item[match_id] == 2):
					await self.startGame()
				break

		if not found:
			nbClient.append({match_id: 1})
			await self.accept()
	async def disconnect(self, close_code):
		global nbClient
		for item in nbClient:
			if self.room_id in item:
				item[self.room_id] -= 1
		await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
	async def chat_message(self, event):
		await self.send(text_data=json.dumps({'message' : event['message']}))

	async def send_message(self, message):
		await self.channel_layer.group_send(self.room_group_name,{"type": "chat_message","message": message,})

	async def getInstancePong(self):
		for pong in self.PongGameList:
			if (self.room_id == pong.idPong):
				return pong

	async def receive(self, text_data):
		if text_data:
			global PongGameList
			jsondata = json.loads(text_data)
			if ("player" in jsondata):
				instance = await self.getInstancePong()
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "down" and jsondata["value"] == True):
				instance.Player1Down = True
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "down" and jsondata["value"] == False):
				instance.Player1Down = False
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "up" and jsondata["value"] == True):
				instance.Player1Up = True
			if ("player" in jsondata and jsondata["player"] == 1 and jsondata["key"] == "up" and jsondata["value"] == False):
				instance.Player1Up = False
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "down" and jsondata["value"] == True):
				instance.Player2Down = True
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "down" and jsondata["value"] == False):
				instance.Player2Down = False
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "up" and jsondata["value"] == True):
				instance.Player2Up = True
			if ("player" in jsondata and jsondata["player"] == 2 and jsondata["key"] == "up" and jsondata["value"] == False):
				instance.Player2Up = False
		else:
			print("Received empty message")


	async def startGame(self):
		await self.send_message({"startGameIn": "Loading"})
		await asyncio.sleep(1)
		game = PongGame(5, 3, {"width": 800, "height": 600}, self, self.room_id)
		asyncio.create_task(game.game_loop())
		self.PongGameList.append(game)
