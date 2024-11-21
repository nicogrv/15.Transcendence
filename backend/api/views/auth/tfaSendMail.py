from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.twoFactorAuthentication import TwoFactorAuthentication
from rest_framework.decorators import api_view


@api_view(['POST'])
def tfaSendMail(req):
    try:
        if (req.user.tfaActive):
            return JsonResponse({'message': '2FA already activated'}, status=status.HTTP_200_OK)
        tfa = TwoFactorAuthentication(player=req.user)
        tfa.save()
        return JsonResponse({'ok': tfa.uid}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': e})
