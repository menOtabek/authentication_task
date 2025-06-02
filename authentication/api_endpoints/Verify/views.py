from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from authentication.api_endpoints.Verify.serializers import VerifyOtpSerializer
from authentication.utils import check_otp_attempts
from authentication.models import Otp


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    @swagger_auto_schema(
        operation_summary='Verify a user',
        operation_description='User verification',
        request_body=VerifyOtpSerializer,
        responses={200: 'User verified successfully', },
        tags=['Verify otp code'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = Otp.objects.filter(
            otp_key=serializer.validated_data['otp_key'],
            otp_code=serializer.validated_data['otp_code']
        ).first()
        check_otp_attempts(Otp.objects.filter(otp_key=serializer.validated_data.get('otp_key')).first(),
                           serializer.validated_data.get('otp_code'))
        if not otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user = otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])

        Otp.objects.filter(user_id=user.id).delete()

        return Response({'result': 'OTP verified'}, status=status.HTTP_200_OK)
