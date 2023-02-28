#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.urls import path,include
from .swagger import schema_view
from apps.study_groups.views import StudentStudyGroupRegsView
from apps.school_extras.views import (
    AddStudentView, UpdateStudentView,
    AddSubjectView, UpdateSubjectView,
    GetSubjectView, AddTeacherView,
    UpdateTeacherView, ListTeachersRegistrationsView,
    ListStudentsRegistrationsView
)


app_name = 'app'

urlpatterns = [
    path('users/', include("apps.users.urls", namespace="users_api")),
    path('subjects/create/', AddSubjectView.as_view(), name='create_subject'),
    path('subjects/<int:subject_id>/', GetSubjectView.as_view(), name='get_subject'),
    path('subjects/<int:subject_id>/update/', UpdateSubjectView.as_view(), name='update_subject'),
    path('students/register/', AddStudentView.as_view(), name='register_student'),
    path('students/<int:student_id>/school_registrations/', ListStudentsRegistrationsView.as_view(), name='student_sch_registrations'),
    path('students/<int:student_id>/study_group_registrations/', StudentStudyGroupRegsView.as_view(), name='student_stdy_grp_registrations'),
    path('students/<int:member_id>/update/', UpdateStudentView.as_view(), name='update_student'),
    path('teachers/register/', AddTeacherView.as_view(), name='register_teacher'),
    path('teachers/<int:teacher_id>/registrations/', ListTeachersRegistrationsView.as_view(), name='teacher_registrations'),
    path('teachers/<int:teacher_reg_id>/update/', UpdateTeacherView.as_view(), name='update_teacher'),
    path('schools/', include("apps.schools.urls", namespace="schools_api")),
    path('events/', include("apps.events.urls", namespace="events_api")),
    path('feedback/', include("apps.feedback.urls", namespace="feedback_api")),
    path('resources/', include("resources.urls", namespace="resources_api")),
    path('sales/', include("apps.sales.urls", namespace="sales_api")),
    path('study_groups/', include("apps.study_groups.urls", namespace="study_groups_api")),
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema_view"),
]
