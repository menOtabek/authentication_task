from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


from authentication.utils import validate_uzbek_phone_number
from authentication.models import User, Otp

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'password')


    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        validate_uzbek_phone_number(phone_number)
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
