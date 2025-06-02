from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from authentication.api_endpoints.UsersList.serializers import UserSerializer
from authentication.models import User
from authentication.role_permissions import is_admin


class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary='Users List',
        operation_description='Get a list of users for admins',
        responses={200: UserSerializer(many=True)},
    )
    @is_admin
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
