from django.urls import path

from .views import (
    UserAPIView,
    AddUserAPIView,
    InvitationsCreateView,
    GetInvitationView,
    UpdateInvitationView,
    GetUserEmailView,
    GetUserAPIView,
    UserDPUploadView,
    UpdateAPIView,
    ChangePasswordView
)

app_name = 'users'

urlpatterns = [
    path('', UserAPIView.as_view(), name='auth_users'),
    path('create/', AddUserAPIView.as_view(), name='add_a_user'),
    path('<int:user_id>/', GetUserAPIView.as_view(), name='get_user_by_id'),
    path('user/<str:email>/', GetUserEmailView.as_view(), name='get_user_by_email'),
    path('invitations/create/', InvitationsCreateView.as_view(), name='invite_users'),
    path('invitations/<int:invite_id>/', GetInvitationView.as_view(), name='get_invite'),
    path('invitations/<int:invite_id>/update/', UpdateInvitationView.as_view(), name='update_invite'),
    path('update/', UpdateAPIView.as_view(), name='update_users'),
    path('update-password/', ChangePasswordView.as_view(), name='update_password'),
    path('dp/', UserDPUploadView.as_view(), name='upload_dp'),
]
