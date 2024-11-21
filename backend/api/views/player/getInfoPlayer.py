from django.http import JsonResponse
from api.serializers.profileSerializer import ProfileSerializer
from api.models.playerModel import Player
from rest_framework import status
from rest_framework.decorators import api_view
from api.models.friendRequestModel import FriendRequest
from api.utils import get_player_or_404


@api_view(['GET'])
def PlayerView(request, pk=None, *args, **kwargs):
    if request.method == 'GET':
        if pk is None:
            user = request.user
            serializer = ProfileSerializer(user)
            is_self = True
            is_friend = False
            request_sent_status = False
        else:
            account, error_response = get_player_or_404(pk)
            if error_response:
                return error_response

            serializer = ProfileSerializer(account)
            user = request.user
            if user != account:
                is_self = False
                if user.are_friends(account):
                    is_friend = True
                    request_sent_status = FriendRequest.ACCEPTED # status 2
                else:
                    is_friend = False
                    if FriendRequest.get_friend_request_or_false(sender=account, receiver=user) != False:
                        request_sent_status = FriendRequest.THEM_SENT_TO_YOU # status 0
                    elif FriendRequest.get_friend_request_or_false(sender=user, receiver=account) != False:
                        request_sent_status = FriendRequest.YOU_SENT_TO_THEM # status 1
                    else:
                        request_sent_status = FriendRequest.NO_REQUEST_SENT # status -1
        response = {
            'data': serializer.data,
            'is_self': is_self,
            'is_friend': is_friend,
            'request_sent_status': request_sent_status
        }
        return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def PlayerStatus(request):
    response = {'status': request.user.get_status()}
    return JsonResponse(response, status=status.HTTP_200_OK)
