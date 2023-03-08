from django.urls import path, include
from apps.events.views import ListSchoolEventsView, ListInvitationsView
from .views import (
    ListSchoolsView,
    GetSchoolView,
    AddSchoolView,
    UpdateSchoolView,
    SchoolsDPView,
)

app_name = 'schools'

urlpatterns = [
    path('', ListSchoolsView.as_view(), name='list_schools'),
    path('<int:school_id>/', GetSchoolView.as_view(), name='get_school'),
    path('create/', AddSchoolView.as_view(), name='register_school'),
    path('<int:school_id>/events/', ListSchoolEventsView.as_view(), name='list_school_events'),
    path('<int:school_id>/update/', UpdateSchoolView.as_view(), name='update_school'),
    path('<int:school_id>/dp-upload/', SchoolsDPView.as_view(), name='school_dp_upload'),
    path('<int:school_id>/', include("apps.school_extras.urls", namespace="school_extras_api")),
    path('<int:school_id>/invitations/', ListInvitationsView.as_view(), name='list_invites'),
]
