from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from api.models.notificationModel import Notification
from api.serializers.friendRequestSerializer import NotificationSerializer
import uuid


@api_view(['GET'])
def fetch_unread_notifications(request):
    user = request.user
    unread_notifications = Notification.objects.filter(recipient=user, read=False)
    serializer = NotificationSerializer(unread_notifications, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def fetch_all_notifications(request):
    user = request.user
    all_notifications = Notification.objects.filter(recipient=user)
    serializer = NotificationSerializer(all_notifications, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)