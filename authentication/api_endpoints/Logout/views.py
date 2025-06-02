from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from authentication.api_endpoints.Logout.serializers import LogoutSerializer
from authentication.models import LocActivity


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    swagger_auto_schema(
        operation_summary='Logout API',
        operation_description='Logout API',
        request_body=LogoutSerializer,
        responses={200: 'User logged out', },
        tags=['Logout']
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        LocActivity.objects.create(user=request.user, activity=LocActivity.ActivityType.LOGOUT)
        print('b ' * 40)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
