from rest_framework import serializers
from django.conf import settings
from api.models.playerModel import Player
from django.core.validators import RegexValidator
from urllib.parse import urlparse
import os
import mimetypes

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['username', 'email']

    def validate_email(self, value):
        user = self.context['request'].user
        User = Player
        email = self.context['request'].data.get('email')
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': f'Email {email} already in use'})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        User = Player
        username = self.context['request'].data.get('username')
        username = serializers.CharField(
            validators=[
                RegexValidator(
                    regex=r'^[^<>=/;]+$',
                    message='Username must not contain <, >, =, /, or ; symbols',
                    code='invalid_username'
                )
            ]
        )
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': f'This username {username} is already in use'})
        return value


    def update(self, instance, validated_data, commit=True):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({'error': 'You cannot edit someone elses profile'})
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        if commit:
            instance.save()
        return instance