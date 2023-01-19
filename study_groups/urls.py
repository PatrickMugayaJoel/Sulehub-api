from django.urls import path
from .views import (
    ListStudyGroupsView,
    CreateStudyGroupView,
    GetStudyGroupView,
    UpdateStudyGroupsView,
    JoinStudyGroupView,
    UpdateRegistrationView
)


app_name = 'study_groups'

urlpatterns = [
    path('', ListStudyGroupsView.as_view(), name='list_study_groups'),
    path('create/', CreateStudyGroupView.as_view(), name='create_study_group'),
    path('student_registration/', JoinStudyGroupView.as_view(), name='join_study_group'),
    path('registrations/<int:study_group_reg_id>/update', UpdateRegistrationView.as_view(), name='sg_reg_update'),
    path('<int:study_group_id>/', GetStudyGroupView.as_view(), name='get_study_group'),
    path('<int:study_group_id>/update/', UpdateStudyGroupsView.as_view(), name='update_study_groups'),
]
