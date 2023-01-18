#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.urls import path,include
from app.swagger import schema_view
from school_extras.views import (
    AddStudentView,
    UpdateStudentView,
    AddSubjectView,
    UpdateSubjectView
)


app_name = 'app'

urlpatterns = [
    path('users/', include("users.urls", namespace="users_api")),
    path('subjects/create/', AddSubjectView.as_view(), name='create_subject'),
    path('subjects/<int:subject_id>/update/', UpdateSubjectView.as_view(), name='update_subject'),
    path('students/register/', AddStudentView.as_view(), name='register_student'),
    path('students/<int:student_reg_id>/update/', UpdateStudentView.as_view(), name='update_student'),
    path('schools/', include("schools.urls", namespace="schools_api")),
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema_view"),
]
