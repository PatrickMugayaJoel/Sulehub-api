from django.urls import path

from .views import (
    ListEventsView,
    ListSchoolEventsView,
    CreateEventView,
    UpdateEventView,
    getEventView
)

app_name = 'events'

urlpatterns = [
    path('', ListEventsView.as_view(), name='list_events'),
    path('<int:school_id>/events', ListSchoolEventsView.as_view(), name='list_school_events'),# goes to schools
    path('create/', CreateEventView.as_view(), name='create_event'),
    path('<int:event_id>/', getEventView.as_view(), name='get_event'),
    path('update/<int:event_id>/', UpdateEventView.as_view(), name='update_event'),
]
