from rest_framework import serializers
from api.models.playerModel import Player
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError({'error': 'Invalid username or password'})
        return data


class LoginFortyTwoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_username(self, username):
        if not Player.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'User not found. Please register first'})
        return username