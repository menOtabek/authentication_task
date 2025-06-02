from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


class AuthenticationRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        exclude_target_urls = [
            reverse('verify-otp'),
            reverse('login'),
            reverse('register'),
        ]
        if request.path.startswith('/api/v1/auth/') and request.path not in exclude_target_urls:
            user = request.user
            print(user, '0' * 40)
            print(user.is_authenticated, '+' * 40)
            if user.is_authenticated is False:
                return JsonResponse(
                    data={'result': "", "error": "Unauthorized access"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return None
