from django.urls import path
from feedback.views import ListResourceFeedbackView
from sales.views import ListResourceSalesView
from .views import (
    ListResourcesView,
    CreateResourceView,
    GetResourceView,
    UpdateResourceView,
    ResourceImageUploadView,
    ResourceFileUploadView
)


app_name = 'resources'

urlpatterns = [
    path('', ListResourcesView.as_view(), name='list_feedback'),
    path('<int:resource_id>/feedback', ListResourceFeedbackView.as_view(), name='list_resource_feedback'),
    path('<int:resource_id>/sales', ListResourceSalesView.as_view(), name='list_resource_sales'),
    path('create/', CreateResourceView.as_view(), name='create_resource'),
    path('<int:resource_id>/', GetResourceView.as_view(), name='get_resource'),
    path('<int:resource_id>/update/', UpdateResourceView.as_view(), name='update_resource'),
    path('<int:resource_id>/image-upload/', ResourceImageUploadView.as_view(), name='resource_image_upload'),
    path('<int:resource_id>/file-upload/', ResourceFileUploadView.as_view(), name='resource_file_upload'),
]
