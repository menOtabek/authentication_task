from rest_framework import serializers


class VerifyOtpSerializer(serializers.Serializer):
    otp_key = serializers.UUIDField()
    otp_code = serializers.CharField(max_length=6)