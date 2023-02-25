from django.urls import path

from .views import (
    ListFeedbackView,
    CreateFeedbackView,
    GetFeedbackView,
    UpdateFeedbackView
)

app_name = 'feedback'

urlpatterns = [
    path('', ListFeedbackView.as_view(), name='list_feedback'),
    path('create/', CreateFeedbackView.as_view(), name='create_feedback'),
    path('<int:feedback_id>/', GetFeedbackView.as_view(), name='get_feedback'),
    path('<int:feedback_id>/update/', UpdateFeedbackView.as_view(), name='update_feedback'),
]
