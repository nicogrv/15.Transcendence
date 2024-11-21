from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator


class ChangePasswordSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'[A-Z]',
                message='Your password must contain at least 1 uppercase letter'
            ),
            RegexValidator(
                regex=r'^[^<>=/;]+$',
                message='Your password must not contain <, >, =, /, or ; symbols'
            )
        ],
        help_text='Required. Must be at least 8 characters long and contain at least 1 uppercase letter')

    def validate(self, data):
        if (data['new_password'] == data['old_password']):
            raise serializers.ValidationError({'password': 'The new password must be different from the old password'})
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'The two passwords fields did not match'})
        return data
