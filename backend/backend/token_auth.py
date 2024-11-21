from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
	# If you are using normal token based authentication
	try:
		token = Token.objects.get(key=token_key)
		return token.user
	except Token.DoesNotExist:
		return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
	def __init__(self, inner):
		super().__init__(inner)

	async def __call__(self, scope, receive, send):
		token_key = "ehbf"

		# if (token_key == None):
		# 	error_message = {'me': 'Token manquant'};
		# 	await send({'type': 'websocket.close', 'code': 1503})
		# 	return
		scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key.decode())
		return await super().__call__(scope, receive, send)