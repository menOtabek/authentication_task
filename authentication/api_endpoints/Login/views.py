from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import LocActivity
from authentication.api_endpoints.Login.serializers import LoginSerializer, TokenSerializer


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

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
        LocActivity.objects.create(user=user, activity=LocActivity.ActivityType.LOGIN)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
