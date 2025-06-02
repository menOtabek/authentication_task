from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from authentication.api_endpoints.Profile.serializers import UserProfileSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_summary='User profile',
        operation_description='Retrieve the authenticated user profile',
        responses={200: UserProfileSerializer()},
        tags=['Profile'],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
