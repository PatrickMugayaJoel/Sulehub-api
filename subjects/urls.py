from django.urls import path

from .views import (
    ListSubjectsView,
    GetSubjectView,
    AddSubjectView,
    UpdateSubjectView,
)

app_name = 'subjects'

urlpatterns = [
    path('', ListSubjectsView.as_view(), name='list_subjects'),
    path('<int:subject_id>/', GetSubjectView.as_view(), name='get_subject'),
    path('create/', AddSubjectView.as_view(), name='create_subject'),
    path('<int:subject_id>/update/', UpdateSubjectView.as_view(), name='update_subject'),
]
