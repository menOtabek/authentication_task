from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from .models import Otp
from .utils import validate_uzbek_phone_number

User = get_user_model()



class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("Invalid phone number or password")

        attrs["user"] = user
        return attrs


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            print('u ' * 40)
            raise serializers.ValidationError(str(e))



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'password')

    def validate_phone_number(self, value):
        validate_uzbek_phone_number(value)
        return value

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.is_verified:
            raise serializers.ValidationError(_('User with this phone number already exists'))
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['otp_key',]


class VerifyOtpSerializer(serializers.Serializer):
    otp_key = serializers.UUIDField()
    otp_code = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'role', 'status', 'created_at']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect")
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        validate_uzbek_phone_number(attrs.get('phone_number'))
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        token = data.get('refresh_token')
        try:
            token = RefreshToken(token)
        except Exception as e:
            token.blacklist()
            raise serializers.ValidationError(str(e))
        if token.get('exp') < timezone.now().timestamp():
            token.blacklist()
            raise serializers.ValidationError(_('Refresh token is expired'))
        return data
