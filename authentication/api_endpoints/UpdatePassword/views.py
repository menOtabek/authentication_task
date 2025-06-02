from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from authentication.api_endpoints.UpdatePassword.serializers import UpdatePasswordSerializer
from authentication.models import LocActivity


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer

    swagger_auto_schema(
        operation_summary='Update password',
        operation_description='Update password',
        request_body=UpdatePasswordSerializer,
        tags=['Update Password'],
    )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        LocActivity.objects.create(user=user, activity=LocActivity.ActivityType.PASSWORD)
        return Response({"result": "Password updated successfully"}, status=status.HTTP_200_OK)
