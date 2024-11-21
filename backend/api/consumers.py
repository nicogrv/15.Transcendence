from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import jwt
import json


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        cookies = self._parse_cookies(self.scope['headers'])
        access_token = cookies.get('access')
        if access_token:
            try:
                payload = jwt.decode(access_token, options={"verify_signature": False})
                user_id = str(payload.get('user_id'))
                self.user_id = user_id
                user = await self.get_user(user_id)
                if user:
                    self.group_name = user_id
                    await self.channel_layer.group_add(
                        self.group_name,
                        self.channel_name
                    )
                    await self.accept()
                    unread_notifications = await self.get_unread_notifications(user)
                    for notification in unread_notifications:
                        sender_id = await self.get_notification_sender_id(notification)
                        sender = await self.get_user(sender_id)
                        await self.send_notification({
                            'message': notification.message,
                            'id': str(notification.id),
                            'sender': {
                                'id': str(sender.id),
                                'username': sender.username,
                                'avatar': sender.avatar
                            },
                            'timestamp': notification.timestamp.isoformat(),
                            'read': notification.read
                        })
                else:
                    await self.close()
            except jwt.DecodeError:
                await self.close(code=4007)
            except ValueError:
                await self.close(code=4008)


    def _parse_cookies(self, headers):
        cookies = {}
        for header in headers:
            if header[0] == b'cookie':
                cookie_header = header[1].decode('utf-8')
                cookie_pairs = cookie_header.split('; ')
                for pair in cookie_pairs:
                    key, value = pair.split('=', 1)
                    cookies[key] = value
        return cookies

    async def disconnect(self, close_code):

        user_id = self.user_id
        user = await self.get_user(user_id)
        print(user)
        await sync_to_async(user.setDeco)()
        if user_id:
            self.group_name = str(user_id)
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


    async def receive_json(self, content):
        message_type = content.get('type')
        notif_id = content.get('notif_id')
        try:
            if message_type == 'friend_request_deleted':
                await self.send_json({
                    'type': 'friend_request_deleted',
                    'message': f'Friend request deleted',
                    'status': 'success',
                    'notif_id': str(notif_id)
                })
            else:
                raise ValueError()
        except Exception as e:
            await self.send_json({
                'type': 'error',
                'message': str(e)
            })


    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))


    async def send_notification(self, event):
        notification_id = event.get('id')
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        read = event['read']

        await self.send_json({
            'type': 'notification',
            'id': str(notification_id),
            'message': message,
            'sender': sender,
            'timestamp': timestamp,
            'read': read
        })
     

    async def friend_request_deleted(self, event):
        notif_id = event.get('notif_id')
        await self.send_json({
            'type': 'friend_request_deleted',
            'message': 'Friend request deleted',
            'status': 'success',
            'notif_id': str(notif_id)
        })


    async def player_joined_tournament(self, event):
        message = event.get('message')
        players = event['players']
        tournois_id = event.get('tournois_id')
        numberOfPlayerNow = event.get('numberOfPlayerNow')
        numberOfPlayer = event.get('numberOfPlayer')

        await self.send_json({
            'type': 'player_joined_tournament',
            'message': message,
            'tournois_id': str(tournois_id),
			'numberOfPlayerNow': numberOfPlayerNow,
			'numberOfPlayer': numberOfPlayer,
            'players': players
        })


    async def match_end(self, event):
        message = event.get('message')
        players = event.get('players')
        match_id = event.get('match_id')
        match_status = event.get('match_status')
        is_tournament = event.get('is_tournament')
        
        await self.send_json({
            'type': 'match_end',
            'message': message,
            'players': players,
            'match_id': match_id,
            'match_status': match_status,
            'is_tournament': is_tournament
        })


    @sync_to_async
    def get_user(self, user_id):
        from api.models.playerModel import Player
        try:
            return Player.objects.get(id=user_id)
        except Player.DoesNotExist:
            return None


    @sync_to_async
    def get_unread_notifications(self, user):
        from api.models.notificationModel import Notification
        unread_notifications = Notification.objects.filter(recipient=user, read=False)
        return list(unread_notifications)
    

    @sync_to_async
    def get_notification(self, notification_id):
        from api.models.notificationModel import Notification
        return Notification.objects.get(pk=notification_id)


    async def mark_notification_as_read(self, notification_id):
        await database_sync_to_async(self._mark_as_read)(notification_id)


    def _mark_as_read(self, notification_id):
        from api.models.notificationModel import Notification
        notification = Notification.objects.get(pk=notification_id)
        notification.read = True
        notification.save(update_fields=['read'])


    @sync_to_async
    def get_notification_sender_id(self, notification):
        return notification.sender.id
