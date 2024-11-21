from rest_framework import serializers
from api.models.playerModel import Player
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[^<>=/;]+$',
                message='Username must not contain <, >, =, /, or ; symbols',
                code='invalid_username'
            )
        ]
    )
    email = serializers.EmailField(required=True, help_text="Required. Add a valid email address")
    password = serializers.CharField(
        write_only=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'[A-Z]',
                message='Your password must contain at least 1 uppercase letter'
            ),
            RegexValidator(
                regex=r'^[^<>=/;]+$',
                message='Your password must not contain <, >, =, /, or ; symbols'
            ),
            validate_password
        ],
        help_text='Required. Must be at least 8 characters long and contain at least 1 uppercase letter'
    )
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Player
        fields = ['username', 'email', 'password', 'confirm_password', 'avatar', 'is_42_user']

    def create(self, validated_data):
        avatar = validated_data.get('avatar', None)
        if avatar is None:
            avatar = "static/avatars/poda.png"
        user = Player (
            email=validated_data['email'],
            username=validated_data['username'],
            avatar = avatar,
        )
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'error': 'The two passwords fields did not match'})
        user.set_password(password)
        user.save()
        return user
