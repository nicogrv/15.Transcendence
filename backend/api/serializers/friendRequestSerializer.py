from rest_framework import serializers
from api.models.friendRequestModel import FriendRequest
from api.models.notificationModel import Notification
from . import profileSerializer


class   FriendRequestSerializer(serializers.ModelSerializer):
    sender = profileSerializer.ProfileSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'sender', 'timestamp']
