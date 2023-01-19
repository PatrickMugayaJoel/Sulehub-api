from django.urls import path

from .views import (
    ListFeedbackView,
    ListResourceFeedbackView,
    CreateFeedbackView,
    getFeedbackView,
    UpdateFeedbackView
)

app_name = 'feedback'

urlpatterns = [
    path('', ListFeedbackView.as_view(), name='list_feedback'),
    path('create/', CreateFeedbackView.as_view(), name='create_feedback'),
    path('<int:feedback_id>/', getFeedbackView.as_view(), name='get_feedback'),
    path('update/<int:feedback_id>/', UpdateFeedbackView.as_view(), name='update_feedback'),
]
