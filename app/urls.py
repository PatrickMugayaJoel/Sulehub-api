#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports.
from django.urls import path,include
from app.swagger import schema_view


app_name = 'app'

urlpatterns = [
    path('users/', include("users.urls", namespace="users_api")),
    path('schools/', include("schools.urls", namespace="schools_api")),
    path('subjects/', include("subjects.urls", namespace="subjects_api")),
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema_view"),
]
