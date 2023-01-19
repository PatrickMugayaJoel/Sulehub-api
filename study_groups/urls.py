from django.urls import path
from .views import (
    ListStudyGroupsView,
    CreateStudyGroupView,
    getStudyGroupView,
    UpdateStudyGroupView,
)


app_name = 'study_groups'

urlpatterns = [
    path('', ListStudyGroupsView.as_view(), name='list_study_groups'),
    path('create/', CreateStudyGroupView.as_view(), name='create_study_group'),
    path('<int:study_groups_id>/', getStudyGroupView.as_view(), name='get_study_group'),
    path('update/<int:study_groups_id>/', UpdateStudyGroupView.as_view(), name='update_study_groups'),
]
