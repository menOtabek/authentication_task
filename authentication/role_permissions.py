from rest_framework import status
from .models import User
from rest_framework.exceptions import ValidationError


def is_admin(func):
    def wrapper(self, request, *args, **kwargs):
        print(request.user.UserRole, 'this is a admin' * 8)
        if not request.user.is_authenticated:
            raise ValidationError('Unauthorized user', status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == User.UserRole.ADMIN:
            return func(self, request, *args, **kwargs)

        raise ValidationError('You have not permission to perform this action.', status.HTTP_403_FORBIDDEN)

    return wrapper
