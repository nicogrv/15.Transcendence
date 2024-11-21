from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.twoFactorAuthentication import TwoFactorAuthentication
from rest_framework.decorators import api_view


@api_view(['POST'])
def tfaSetActive(req):
    data = req.data
    try:
        elem = TwoFactorAuthentication.objects.get(uid=data["id"], player=req.user)
        if (elem.is_expired() or not elem.checkCode(data["code"])):
            return JsonResponse({'error': 'Problem with code'}, status=status.HTTP_400_BAD_REQUEST)
        req.user.tfaActive = True
        req.user.save()
        return JsonResponse({'message': '2FA method was activated successfully'}, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': 'Error while 2FA method activation'}, status=status.HTTP_400_BAD_REQUEST)
