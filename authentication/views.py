from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from .utils import generate_otp_code, check_otp_attempts, send_telegram_otp_code
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    swagger_auto_schema(
        operation_summary='Login API',
        operation_description='Login API',
        request_body=LoginSerializer,
        responses={200: TokenSerializer()},
        tags=['Login']
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    swagger_auto_schema(
        operation_summary='Logout API',
        operation_description='Logout API',
        request_body=LogoutSerializer,
        responses={200: LogoutSerializer()},
        tags=['Logout']
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('bu ' * 40)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary='Register a user',
        operation_description='User registration',
        responses={201: OtpSerializer()},
        request_body=RegisterSerializer,
        tags=['Authentication'],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_serializer = serializer.save()
        otp_code = generate_otp_code()
        otp = Otp.objects.create(user_id=validated_serializer.id, otp_code=otp_code)
        otp.save()
        send_telegram_otp_code(otp)
        return Response(OtpSerializer(otp).data, status=status.HTTP_201_CREATED)


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    @swagger_auto_schema(
        operation_summary='Verify a user',
        operation_description='User verification',
        request_body=VerifyOtpSerializer,
        responses={200: UserProfileSerializer()},
        tags=['Authentication'])
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
            return Response({"error": "Invalid OTP"}, status=400)

        user = otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])

        Otp.objects.filter(user_id=user.id).delete()

        return Response({'result': 'OTP verified'}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    swagger_auto_schema(
        operation_summary='User profile',
        operation_description='User profile',
        responses={200: UserProfileSerializer()},
        tags=['Profile'],
    )

    def get_object(self):
        return self.request.user


class RefreshTokenView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    swagger_auto_schema(
        operation_summary='Refresh token',
        operation_description='Refresh token',
        request_body=RefreshTokenSerializer,
        responses={200: TokenSerializer()},
        tags=['Refresh'],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken(serializer.validated_data.get('refresh_token'))
        user_id = refresh.payload.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('User not found')
        new_refresh_token = RefreshToken.for_user(user)
        new_access_token = new_refresh_token.access_token
        return Response({'access_token': new_access_token, 'refresh_token': new_refresh_token},
                        status=status.HTTP_200_OK)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    swagger_auto_schema(
        operation_summary='Update password',
        operation_description='Update password',
        request_body=UpdatePasswordSerializer,
        tags=['UpdatePassword'],
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"result": "Password updated successfully"}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    swagger_auto_schema(
        operation_summary='Reset password',
        operation_description='Reset password',
        request_body=ResetPasswordSerializer,
        responses={200: ResetPasswordSerializer()},
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = Otp.objects.filter(
            otp_key=serializer.validated_data['otp_key'],
            otp_code=serializer.validated_data['otp_code']
        ).first()
        if not otp:
            return Response({"error": "Invalid OTP"}, status=400)

        user = otp.user
        user.password = make_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"result": "Password reset successfully"}, status=status.HTTP_200_OK)
