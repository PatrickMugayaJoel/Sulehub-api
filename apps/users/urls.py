from django.urls import path

from .views import (
    UserAPIView,
    RegistrationAPIView,
    InvitationsView,
    GetInvitationView,
    ListInvitationsView,
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
    path('invitations/create', InvitationsView.as_view(), name='invite_users'),
    path('invitations/<int:invite_id>/', GetInvitationView.as_view(), name='get_invite'),
    path('invitations/', ListInvitationsView.as_view(), name='list_invites'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UpdateAPIView.as_view(), name='update_users'),
    path('update-password/', ChangePasswordView.as_view(), name='update_password'),
    path('dp/', UserDPUploadView.as_view(), name='upload_dp'),
]
