from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from api.models.playerModel import Player
from api.models.friendRequestModel import FriendRequest
from api.serializers.friendRequestSerializer import FriendRequestSerializer
from api.serializers.profileSerializer import ProfileSerializer
from api.models.notificationModel import Notification
from django.db import transaction
from api.utils import get_player_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@api_view(['GET'])
def SearchView(request, *args, **kwrgs):
    search_query = request.GET.get('query', '')
    if not search_query:
        return JsonResponse({'message': 'No query provided'}, status=status.HTTP_200_OK)
    
    accounts = []
    search_results = Player.objects.filter(username__icontains=search_query)
    if search_results.exists():
        serializer = ProfileSerializer(search_results, many=True)
        accounts = serializer.data
        user = request.user

        for account in accounts:
            account_player = Player.objects.get(id=account['id'])
            account['is_self'] = account_player.id == user.id
            account['is_friend'] = user.are_friends(account_player)

        response = {'accounts': accounts}
        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'accounts': accounts, 'message': 'Player not found'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def FriendsList(request, pk):
    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    friends = user.get_friends()
    requests = []
    if user == request.user:
        requests = FriendRequest.objects.filter(receiver=request.user, status_request=FriendRequest.ACCEPTED)
        requests = FriendRequestSerializer(requests, many=True).data

    return JsonResponse({
        'player': ProfileSerializer(user).data,
        'friends': ProfileSerializer(friends, many=True).data,
        'requests': requests
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserIDbyUsername(request, username):
    try:
        user = Player.objects.get(username=username)
        return JsonResponse({'id': user.pk}, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return JsonResponse({'message': 'Are you sure? This Player does not exist'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def SendFriendRequest(request, pk):
    if pk == request.user.id:
        return JsonResponse({'message': 'Cannot send a friend request to yourself'}, status=status.HTTP_200_OK)

    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    if request.user.are_friends(user):
        return JsonResponse({'message': 'You are already friends'}, status=status.HTTP_200_OK)

    check1 = FriendRequest.objects.filter(receiver=request.user, sender=user)
    check2 = FriendRequest.objects.filter(receiver=user, sender=request.user)

    if not check1.exists() and not check2.exists():
        FriendRequest.objects.create(receiver=user, sender=request.user)
        notification = Notification.objects.create(recipient=user, message=f'You just received a new friend request from {request.user.username}', sender=request.user)
        notification.save()
        return JsonResponse({'message': 'Friend request is sent!'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Oops! Friend request is already sent by this Player to you'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def AcceptFriendRequest(request, pk):
    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    friend_request = FriendRequest.objects.filter(sender=user, receiver=request.user).first()

    if friend_request is None:
        return JsonResponse({'message': 'No pending friend request found'}, status=status.HTTP_200_OK)

    friend_request.status_request = FriendRequest.ACCEPTED # status 2
    friend_request.save(update_fields=['status_request'])


    user.add_friend(request.user)

    notification_to_recipient = Notification.objects.filter(sender=user, recipient=request.user).first()
    if notification_to_recipient:
        notification_to_recipient.read = True
        tmp = str(notification_to_recipient)
        notification_to_recipient.save(update_fields=['read'])
        tmp = str(notification_to_recipient.id)

    notification_to_sender = Notification.objects.create(recipient=user, message='Your friend request has been accepted', sender=request.user)
    notification_to_sender.read = True
    notification_to_sender.save()

    notifications_to_delete = Notification.objects.filter(sender=user, recipient=request.user)
    for notification in notifications_to_delete:
        notification.delete()

    return JsonResponse({'message': 'Friend request accepted', 'id': tmp}, status=status.HTTP_200_OK)



@api_view(['POST'])
def RejectFriendRequest(request, pk):
    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    friend_request = FriendRequest.objects.filter(sender=user, receiver=request.user).first()

    if friend_request is None:
        return JsonResponse({'message': 'No pending friend request found'}, status=status.HTTP_200_OK)
    
    friend_request.status_request = FriendRequest.REJECTED # status 3
    friend_request.save(update_fields=['status_request'])
    friend_request.delete()

    notification_to_recipient = Notification.objects.filter(sender=user, recipient=request.user).first()
    if notification_to_recipient:
        notification_to_recipient.read = True
        notification_to_recipient.save(update_fields=['read'])
        tmp = str(notification_to_recipient.id)
        groupe_name = f'{request.user.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            groupe_name,
            {
                "type": "friend_request_deleted",
                "notif_id": str(notification_to_recipient.id)
            }
        )
        tmp = str(notification_to_recipient.id)
        groupe_name = f'{request.user.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            groupe_name,
            {
                "type": "friend_request_deleted",
                "notif_id": str(notification_to_recipient.id)
            }
        )
        notification_to_recipient.delete()
        return JsonResponse({'message': 'Friend request rejected', 'id': tmp}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Notification not found'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def CancelFriendRequest(request, pk):
    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    friend_request = FriendRequest.objects.filter(sender=request.user, receiver=user).first()
    if friend_request is None:
        return JsonResponse({'message': 'No pending friend request found'}, status=status.HTTP_200_OK)
    else:
        friend_request.delete()

    notification = Notification.objects.filter(sender=request.user, recipient=user).first()
    if notification:
        notification.read = True
        notification.save(update_fields=['read'])
        groupe_name = f'{user.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            groupe_name,
            {
                "type": "friend_request_deleted",
                "notif_id": str(notification.id)
            }
        )
        notification.delete()
        return JsonResponse({'message': 'Friend request canceled'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Notification not found'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def UnfriendView(request, pk):
    user, error_response = get_player_or_404(pk)
    if error_response:
        return error_response

    with transaction.atomic():
        request.user.unfriend(user)
        user.unfriend(request.user)

        FriendRequest.objects.filter(sender=request.user, receiver=user, status_request=FriendRequest.ACCEPTED).delete()
        FriendRequest.objects.filter(sender=user, receiver=request.user, status_request=FriendRequest.ACCEPTED).delete()

    return JsonResponse({'message': 'Unfriended successfully'}, status=status.HTTP_200_OK)
