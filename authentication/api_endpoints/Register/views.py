from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from authentication.api_endpoints.Register.serializers import OtpSerializer, RegisterSerializer
from authentication.models import Otp, User
from authentication.utils import generate_otp_code, send_telegram_otp_code


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary='Register a user',
        operation_description='User registration',
        responses={201: OtpSerializer()},
        request_body=RegisterSerializer,
        tags=['Register'],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_serializer = serializer.save()
        otp_code = generate_otp_code()
        otp = Otp.objects.create(user_id=validated_serializer.id, otp_code=otp_code)
        otp.save()
        send_telegram_otp_code(otp)
        return Response(OtpSerializer(otp).data, status=status.HTTP_201_CREATED)
