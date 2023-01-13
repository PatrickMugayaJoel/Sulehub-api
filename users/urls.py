from django.urls import path

from .views import (
    UserAPIView,
    RegistrationAPIView,
    LoginView,
    LogoutView
)

app_name = 'users'

urlpatterns = [
    path('', UserAPIView.as_view(), name='auth_users'),
    path('register/', RegistrationAPIView.as_view(), name='register_users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
