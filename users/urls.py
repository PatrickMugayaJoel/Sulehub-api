from django.urls import path

from .views import (
    UserAPIView,
    RegistrationAPIView,
    LoginView,
    LogoutView,
    GetUserAPIView,
    UserDPUploadView,
    UpdateAPIView,
    ChangePasswordView
)

app_name = 'users'

urlpatterns = [
    path('', UserAPIView.as_view(), name='auth_users'),
    path('<int:user_id>/', GetUserAPIView.as_view(), name='get_user'),
    path('register/', RegistrationAPIView.as_view(), name='register_users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UpdateAPIView.as_view(), name='update_users'),
    path('update-password/', ChangePasswordView.as_view(), name='update_password'),
    path('dp/', UserDPUploadView.as_view(), name='upload_dp'),
]
