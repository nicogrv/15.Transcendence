from rest_framework import serializers
from api.models.playerModel import Player


class ProfileSerializer(serializers.ModelSerializer):
    status_profile_str = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    class Meta:
        model = Player
        fields = [
            'username',
            'email',
            'id',
            'status_profile_str',
            'date_joined',
            'avatar',
            'friend_count',
            'elo',
            'victories', # games won
            'defeats', # games lost
            'games_played',
            'score',
            'tournaments_won',
            'is_42_user',
            'tfaActive'
        ]

    def get_status_profile_str(self, obj):
        return obj.get_status_profile_display()

    def get_date_joined(self, obj):
        return obj.get_formatted_date_joined()

