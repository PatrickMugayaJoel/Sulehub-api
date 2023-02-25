from django.urls import path

from .views import (
    ListSubjectsView,
    ## Teachers
    ListTeachersView,
    ListTeacherStudentsView,
    ListTeacherSubjectsView,
    ## Students
    ListStudentsView,
    ListStudentSubjectsView
)

app_name = 'subjects'

urlpatterns = [
    ## Subjects
    path('subjects/', ListSubjectsView.as_view(), name='list_subjects'),

    ## Teachers
    path('teachers/', ListTeachersView.as_view(), name='list_teachers'),
    path('teachers/<int:teacher_reg_id>/students/', ListTeacherStudentsView.as_view(), name='get_teacher_students'),
    path('teachers/<int:teacher_reg_id>/subjects/', ListTeacherSubjectsView.as_view(), name='get_teacher_subjects'),

    ## Students
    path('students/', ListStudentsView.as_view(), name='list_students'),
    path('students/<int:member_id>/subjects/', ListStudentSubjectsView.as_view(), name='get_student_subjects'),
]
