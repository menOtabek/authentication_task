from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status


class AuthenticationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        exclude_target_urls = [
            reverse('verify-otp'),
            reverse('login'),
            reverse('register'),
        ]

        try:
            user_auth_tuple = self.jwt_auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
        except Exception as e:
            return JsonResponse(
                data={"detail": f"Invalid token: {str(e)}"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.path.startswith('/api/v1/auth/') and request.path not in exclude_target_urls:
            print(request.path)
            print(request.user)
            print(request.user.is_authenticated)
            if not getattr(request, 'user', None) or not request.user.is_authenticated:
                return JsonResponse(
                    data={"detail": "Authentication required"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return self.get_response(request)
