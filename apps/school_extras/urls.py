from django.urls import path

from .views import (
    ListSubjectsView,
    ListTeachersView,
    ListStudentsView,
    ListLevelsView,
)

app_name = 'subjects'

urlpatterns = [
    ## Subjects
    path('subjects/', ListSubjectsView.as_view(), name='list_subjects'),

    ## Teachers
    path('teachers/', ListTeachersView.as_view(), name='list_teachers'),

    ## Students
    path('students/', ListStudentsView.as_view(), name='list_students'),

    ## Levels
    path('levels/', ListLevelsView.as_view(), name='list_levels'),

]
