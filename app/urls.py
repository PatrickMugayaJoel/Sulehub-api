#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.urls import path,include
from app.swagger import schema_view
from study_groups import ListStudentStudyGroupsView
from school_extras.views import (
    AddStudentView, UpdateStudentView,
    AddSubjectView, UpdateSubjectView,
    GetSubjectView, AddTeacherView,
    UpdateTeacherView, ListTeachersRegistrationsView,
    ListStudentsRegistrationsView
)


app_name = 'app'

urlpatterns = [
    path('users/', include("users.urls", namespace="users_api")),
    path('subjects/create/', AddSubjectView.as_view(), name='create_subject'),
    path('subjects/<int:subject_id>/', GetSubjectView.as_view(), name='get_subject'),
    path('subjects/<int:subject_id>/update/', UpdateSubjectView.as_view(), name='update_subject'),
    path('students/register/', AddStudentView.as_view(), name='register_student'),
    path('students/<int:student_id>/study_groups', ListStudentStudyGroupsView.as_view(), name='list_students_study_groups'),
    path('students/<int:student_id>/registrations/', ListStudentsRegistrationsView.as_view(), name='student_registrations'),
    path('students/<int:student_reg_id>/update/', UpdateStudentView.as_view(), name='update_student'),
    path('teachers/register/', AddTeacherView.as_view(), name='register_teacher'),
    path('teachers/<int:teacher_id>/registrations/', ListTeachersRegistrationsView.as_view(), name='teacher_registrations'),
    path('teachers/<int:teacher_reg_id>/update/', UpdateTeacherView.as_view(), name='update_teacher'),
    path('schools/', include("schools.urls", namespace="schools_api")),
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema_view"),
]
