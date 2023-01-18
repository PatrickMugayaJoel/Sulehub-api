from django.urls import path

from .views import (
    ## Subjects
    ListSubjectsView,
    GetSubjectView,
    ## Teachers
    ListTeachersView,
    AddTeacherView,
    UpdateTeacherView,
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
    path('subjects/<int:subject_id>/', GetSubjectView.as_view(), name='get_subject'),

    ## Teachers
    path('teachers/', ListTeachersView.as_view(), name='list_teachers'),
    path('teachers/register/', AddTeacherView.as_view(), name='register_teacher'),
    path('teachers/<int:teacher_reg_id>/update/', UpdateTeacherView.as_view(), name='update_teacher'),
    path('teachers/<int:teacher_reg_id>/students/', ListTeacherStudentsView.as_view(), name='get_teacher_students'),
    path('teachers/<int:teacher_reg_id>/subjects/', ListTeacherSubjectsView.as_view(), name='get_teacher_subjects'),
    # TODO: endpoint for all subjects independent of school (Should be put in users.url)
    ###########################
    ## For getting registration specific info, else use get_user endpoint.
    ###########################
    # path('teachers/<int:teacher_id>/', GetTeacherView.as_view(), name='get_teacher'),

    ## Students
    path('students/', ListStudentsView.as_view(), name='list_students'),
    path('students/<int:student_reg_id>/subjects/', ListStudentSubjectsView.as_view(), name='get_student_subjects'),
    # TODO: endpoint for all subjects independent of school (Should be put in users.url)
    ###########################
    ## For getting registration specific info, else use get_user endpoint.
    ###########################
    # path('students/<int:student_id>/', GetStudentView.as_view(), name='get_student'),
]
