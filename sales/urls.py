from django.urls import path
from .views import (
    ListSalesView,
    getSalesView,
    UpdateSalesView,
)


app_name = 'sales'

urlpatterns = [
    path('', ListSalesView.as_view(), name='list_sales'),
    path('<int:sale_id>/', getSalesView.as_view(), name='get_sale'),
    path('update/<int:sale_id>/', UpdateSalesView.as_view(), name='update_sale'),
]
