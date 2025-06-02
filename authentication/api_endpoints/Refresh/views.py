from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, LocActivity
from authentication.api_endpoints.Refresh.serializers import RefreshTokenSerializer, TokenSerializer


class RefreshTokenView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer

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
        LocActivity.objects.create(user=user, activity=LocActivity.ActivityType.REFRESH)
        return Response({'access_token': new_access_token, 'refresh_token': new_refresh_token},
                        status=status.HTTP_200_OK)
