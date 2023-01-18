from django.urls import path, include

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
    path('register/', AddSchoolView.as_view(), name='register_school'),
    path('<int:school_id>/update/', UpdateSchoolView.as_view(), name='update_school'),
    path('<int:school_id>/dp-upload/', SchoolsDPView.as_view(), name='school_dp_upload'),
    path('<int:school_id>/', include("school_extras.urls", namespace="school_extras_api")),
]
