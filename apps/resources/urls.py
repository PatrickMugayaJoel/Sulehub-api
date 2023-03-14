from django.urls import path
from django_downloadview import ObjectDownloadView
from apps.feedback.views import ListResourceFeedbackView
from apps.sales.views import ListResourceSalesView
from .models import Resource
from .views import (
    ListResourcesView,
    CreateResourceView,
    GetResourceView,
    UpdateResourceView,
    ResourceImageUploadView,
    ResourceFileUploadView
)


app_name = 'resources'

# https://github.com/jazzband/django-downloadview/tree/master/demo/demoproject/object
file = ObjectDownloadView.as_view(model=Resource, file_field='_file')
image = ObjectDownloadView.as_view(model=Resource, file_field='image')

urlpatterns = [
    path('', ListResourcesView.as_view(), name='list_feedback'),
    path('<int:resource_id>/feedback/', ListResourceFeedbackView.as_view(), name='list_resource_feedback'),
    path('<int:resource_id>/sales/', ListResourceSalesView.as_view(), name='list_resource_sales'),
    path('create/', CreateResourceView.as_view(), name='create_resource'),
    path('<int:resource_id>/', GetResourceView.as_view(), name='get_resource'),
    path('<int:resource_id>/update/', UpdateResourceView.as_view(), name='update_resource'),
    path('<int:resource_id>/image-upload/', ResourceImageUploadView.as_view(), name='resource_image_upload'),
    path('<int:resource_id>/file-upload/', ResourceFileUploadView.as_view(), name='resource_file_upload'),
    path('<int:resource_id>/image-download/', image, name='resource_image_download'),
    path('<int:resource_id>/file-download/', file, name='resource_file_download'),
]
