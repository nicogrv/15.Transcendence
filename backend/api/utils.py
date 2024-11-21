from api.models.playerModel import Player
from django.http import JsonResponse
from rest_framework import status
from asgiref.sync import sync_to_async
from django.db.models import F


def get_player_or_404(pk):
    try:
        player = Player.objects.get(id=pk)
        return player, None
    except Player.DoesNotExist:
        return None, JsonResponse({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)


# calculer l'elo pour chaque player. La fonction called in endGame,

@sync_to_async
def update_stats(player1, player2, score_player1, score_player2, winner):
    k = 20 # elo constant

    new_elo_player1 = player1.elo + k * (score_player1 - score_player2)
    new_elo_player2 = player2.elo + k * (score_player2 - score_player1)

    new_elo_player1 = max(0, new_elo_player1)
    new_elo_player2 = max(0, new_elo_player2)
    
    player1_elo = round(new_elo_player1)
    player2_elo = round(new_elo_player2)

    if winner == player1:
        player1_victories = F('victories') + 1
        player2_defeats = F('defeats') + 1
    else:
        player1_defeats = F('defeats') + 1
        player2_victories = F('victories') + 1
    
    Player.objects.filter(id=player1.id).update(
        score=F('score') + score_player1,
        elo=player1_elo,
        games_played=F('games_played') + 1,
        status_profile=Player.STATUS.ONLINE,
        victories=player1_victories if winner == player1 else F('victories'),
        defeats=player1_defeats if winner != player1 else F('defeats')
    )

    Player.objects.filter(id=player2.id).update(
        score=F('score') + score_player2,
        elo=player2_elo,
        games_played=F('games_played') + 1,
        status_profile=Player.STATUS.ONLINE,
        victories=player2_victories if winner == player2 else F('victories'),
        defeats=player2_defeats if winner != player2 else F('defeats')
    )