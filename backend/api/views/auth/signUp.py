
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from api.models.playerModel import Player
from api.serializers.registerSerializer import RegisterSerializer
from api import tokenTools


@api_view(['POST'])
@authentication_classes([]) # for allowing unauthenticated users
@permission_classes([AllowAny]) # for allowing unauthenticated users
def signUp(request, user_data=None):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email =  serializer.validated_data.get('email')
            is_42_user = serializer.validated_data.get('is_42_user', False)
            if Player.objects.filter(username=username).exists() and Player.objects.filter(email=email).exists():
                return JsonResponse({'error': 'You have already sign up with this account information'}, status=status.HTTP_400_BAD_REQUEST)

            if Player.objects.filter(username=username).exists():
                return JsonResponse({'error': f'Username {username} already in use'}, status=status.HTTP_400_BAD_REQUEST)

            if Player.objects.filter(email=email).exists():
                return JsonResponse({'error': f'Email {email} already in use'}, status=status.HTTP_400_BAD_REQUEST)

            newPlayer = serializer.save()
            if is_42_user:
                newPlayer.is_42_user = True
                newPlayer.save()
            newPlayer = authenticate(username=username, password=serializer.validated_data['password'])
            return tokenTools.cookie_tokens(request, newPlayer)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
