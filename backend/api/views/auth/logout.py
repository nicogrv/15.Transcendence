
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt import tokens
from api.models.playerModel import Player


@api_view(['POST'])
def playerLogout(request):
    if request.method == 'POST':
        # Delete the token to log out the user
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        if refresh_token:
            token = tokens.RefreshToken(refresh_token)
            token.blacklist()
            res = JsonResponse({'message': 'Logout successfully.'}, status=status.HTTP_200_OK) # should redirect at home page)
        
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            res["X-CSRFToken"] = None
            res["csrftoken"] = None
            request.user.status_profile = Player.STATUS.OFFLINE
            request.user.save(update_fields=['status_profile'])
            return res
        JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
