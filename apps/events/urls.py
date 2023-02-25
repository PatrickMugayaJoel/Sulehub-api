from django.urls import path

from .views import (
    ListEventsView,
    CreateEventView,
    UpdateEventView,
    GetEventView
)

app_name = 'events'

urlpatterns = [
    path('', ListEventsView.as_view(), name='list_events'),
    path('create/', CreateEventView.as_view(), name='create_event'),
    path('<int:event_id>/', GetEventView.as_view(), name='get_event'),
    path('<int:event_id>/update/', UpdateEventView.as_view(), name='update_event'),
]
