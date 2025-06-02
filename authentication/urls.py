from django.urls import path
from authentication.api_endpoints import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyOtpView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('users/', UsersListAPIView.as_view(), name='users-list'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
]
