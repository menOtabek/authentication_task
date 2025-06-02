from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        token = data.get('refresh_token')
        try:
            token = RefreshToken(token)
        except Exception as e:
            token.blacklist()
            raise serializers.ValidationError(str(e))
        if token.get('exp') and token.get('exp') < timezone.now().timestamp():
            raise serializers.ValidationError('Refresh token is expired')
        return data


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
