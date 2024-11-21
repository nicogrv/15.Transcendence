from django.http import JsonResponse
from api.models.playerModel import Player
from api.serializers.editProfileSerializer import EditProfileSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from api.utils import get_player_or_404
from asgiref.sync import async_to_sync, sync_to_async
import random
import string
import os


def generate_random_string(length=36):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def handle_uploaded_file(f, user):
    try:
        os.remove(user.avatar)
    except:
        pass
    randomStr = generate_random_string()
    with open(f"static/avatars/{randomStr}.png", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    user.avatar = f"static/avatars/{randomStr}.png"
    user.save()

@api_view(['POST'])
def EditProfile(request, pk):
    if request.method == 'POST':
        user = Player.objects.get(id=pk)
        if ("avatar" in request.FILES):
            handle_uploaded_file(request.FILES["avatar"], user)
        serializer = EditProfileSerializer(user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Profile edit successfully'}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ChangeStatus(request, pk):
    if request.method == 'POST':
        user, error_response = get_player_or_404(pk)
        if error_response:
            return error_response

        if user.status_profile == Player.STATUS.ONLINE:
            user.status_profile = Player.STATUS.PLAYING
            user.save(update_fields=['status_profile'])
            return JsonResponse({'message': 'Status was updated to Playing'}, status=status.HTTP_200_OK)

        elif user.status_profile == Player.STATUS.PLAYING:
            user.status_profile = Player.STATUS.ONLINE
            user.save(update_fields=['status_profile'])
            return JsonResponse({'message': 'Status was updated to Online'}, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def changeStatusRefresh(request, pk):
    if request.method == 'POST':
        user, error_response = get_player_or_404(pk)
        if error_response:
            return error_response

        if user.status_profile == Player.STATUS.ONLINE or user.status_profile == Player.STATUS.PLAYING:
            user.status_profile = Player.STATUS.OFFLINE
            user.save(update_fields=['status_profile'])
            return JsonResponse({'message': 'Status was updated to Offline'}, status=status.HTTP_200_OK)

        elif user.status_profile == Player.STATUS.OFFLINE:
            user.status_profile = Player.STATUS.ONLINE
            user.save(update_fields=['status_profile'])
            return JsonResponse({'message': 'Status was updated to Online'}, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)