from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import update_session_auth_hash
from api.serializers.changePasswordSerializer import ChangePasswordSerializer


@api_view(['POST'])
def ChangePassword(request, pk):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            if user.id != pk:
                return JsonResponse({'error': 'You dont have permission for this user'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save(update_fields=['password'])
                update_session_auth_hash(request, user) # Important! To update the session with the new password
                return JsonResponse({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            return JsonResponse({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
