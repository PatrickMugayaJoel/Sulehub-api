from django.urls import path
from feedback.views import ListResourceFeedbackView
from sales.views import ListResourceSalesView
from .views import (
    ListResourcesView,
    ListResourceFeedbackView,
    CreateResourceView,
    getResourceView,
    UpdateResourceView,
    buyResourceView
)


app_name = 'resources'

urlpatterns = [
    path('', ListResourcesView.as_view(), name='list_feedback'),
    path('<int:resource_id>/feedback', ListResourceFeedbackView.as_view(), name='list_resource_feedback'),
    path('<int:resource_id>/sales', ListResourceSalesView.as_view(), name='list_resource_sales'),
    path('create/', CreateResourceView.as_view(), name='create_resource'),
    path('<int:resource_id>/', getResourceView.as_view(), name='get_resource'),
    path('<int:resource_id>/buy', buyResourceView.as_view(), name='buy_resource'),
    path('update/<int:resource_id>/', UpdateResourceView.as_view(), name='update_resource'),
]
