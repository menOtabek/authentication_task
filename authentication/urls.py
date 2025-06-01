from django.urls import path
from .views import RegisterView, VerifyOtpView, ProfileView, UpdatePasswordView, ResetPasswordView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
