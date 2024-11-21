from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.models.notificationModel import Notification


@receiver(post_save, sender=Notification)
def notification_created(instance, created, **kwargs):
    if created:
        recipient = instance.recipient
        group_name = f'{recipient.pk}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_add)(
            group_name,
            f'user_{recipient.pk}'
        )
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "id": str(instance.pk),
                "message": instance.message,
                "sender": {
                    "id": str(instance.sender.pk),
                    "username": instance.sender.username,
                    "avatar": instance.sender.avatar
                },
                "timestamp": instance.timestamp.isoformat(),
                "read": instance.read
            }
        )
