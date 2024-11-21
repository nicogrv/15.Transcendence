from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from api.serializers.loginSerializer import LoginSerializer
from api.models.twoFactorAuthentication import TwoFactorAuthentication
from api import tokenTools


@api_view(['POST'])
@permission_classes([AllowAny])
def signIn(request, **kwargs):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if (user.tfaActive and not request.data["tfa"]):
                    code = TwoFactorAuthentication(player=user)
                    code.save()
                    return JsonResponse({'tfa': code.uid})
                elif (user.tfaActive and request.data["tfa"]):
                    elem = TwoFactorAuthentication.objects.get(uid=request.data["uid"], player=user)
                    if (elem.is_expired() or not elem.checkCode(request.data["tfa"])):
                        return JsonResponse({'error' : 'Problem with the code'}, status=status.HTTP_400_BAD_REQUEST)
                return tokenTools.cookie_tokens(request, user)
            else:
                return JsonResponse({'error': 'Invalid username or password. Please try again'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)