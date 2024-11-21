from django.http import JsonResponse
from api.models.playerModel import Player
from api.models.playerTournament import playerTournament
from api.models.tournament import Tournament
from api.models.match import Match
from api.serializers.matchSerializer import TournamentSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q, Avg
from api.utils import get_player_or_404


def get_metrics():
    elo_ratings = Player.objects.values_list('elo', flat=True)
    mean_elo = elo_ratings.aggregate(Avg('elo'))['elo__avg']
    rounded_mean_elo = round(mean_elo)

    score_ratings = Player.objects.values_list('score', flat=True)
    mean_score = score_ratings.aggregate(Avg('score'))['score__avg']
    rounded_mean_score = round(mean_score)

    games_played_count = Player.objects.values_list('games_played', flat=True)
    mean_games_played = games_played_count.aggregate(Avg('games_played'))['games_played__avg']
    rounded_mean_games_played = round(mean_games_played)

    victories_count = Player.objects.values_list('victories', flat=True)
    mean_victories = victories_count.aggregate(Avg('victories'))['victories__avg']
    rounded_mean_victories = round(mean_victories)

    defeats_count = Player.objects.values_list('defeats', flat=True)
    mean_defeats = defeats_count.aggregate(Avg('defeats'))['defeats__avg']
    rounded_mean_defeats = round(mean_defeats)

    tournaments_won_count = Player.objects.values_list('tournaments_won', flat=True)
    mean_tournaments_won = tournaments_won_count.aggregate(Avg('tournaments_won'))['tournaments_won__avg']
    rounded_mean_tournaments_won = round(mean_tournaments_won)

    metrics_data = {
        'mean_elo': rounded_mean_elo,
        'mean_games_played': rounded_mean_games_played,
        'mean_victories': rounded_mean_victories,
        'mean_defeats': rounded_mean_defeats,
        'mean_tournaments_won': rounded_mean_tournaments_won,
        'mean_score': rounded_mean_score
    }

    return metrics_data


@api_view(['GET'])
def DashboardView(request, pk):
    if request.method == 'GET':
        player, error_response = get_player_or_404(pk)
        if error_response:
            return error_response

        status_filter = request.query_params.get('status', 'FINISH')
        matches = Match.objects.filter(
            (Q(player1=player) | Q(player2=player)) & Q(status=status_filter)
        ).order_by('-start_time')

        metrics_data = get_metrics()
        match_data = []
        for match in matches:
            match_json = match.json()
            match_data.append(match_json)
        response = {
            'player': str(player),
            'elo': player.elo,
            'score': getattr(player, 'score', 0),
            'wins': getattr(player, 'victories', 0),
            'losses': getattr(player, 'defeats', 0),
            'games_played': getattr(player, 'games_played', 0),
            'tournaments_won': getattr(player, 'tournaments_won', 0),
            'matches': match_data,
            'metrics_data': metrics_data
        }
        return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def TournamentsList(request, pk):
    if request.method == 'GET':
        player, error_response = get_player_or_404(pk)
        if error_response:
            return error_response

        status_filter = request.query_params.get('status', 2)
        player_tournaments = playerTournament.objects.filter(player=player)
        tournaments = Tournament.objects.filter(
            Q(id__in=[pt.Tournament.id for pt in player_tournaments]) & Q(status=status_filter)
        ).order_by('-date_joined')

        serializer = TournamentSerializer(tournaments, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def MatchList(request, pk):
    if request.method == 'GET':
        player, error_response = get_player_or_404(pk)
        if error_response:
            return error_response

        status_filter = request.query_params.get('status', 'FINISH')
        matches = Match.objects.filter(
            (Q(player1=player) | Q(player2=player)) & Q(status=status_filter)
        ).order_by('-start_time')

        match_data = []
        for match in matches:
            match_json = match.json()
            match_data.append(match_json)

        response = {'matches': match_data}
        return JsonResponse(response, status=status.HTTP_200_OK)
