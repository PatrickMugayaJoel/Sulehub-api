from django.urls import path
from .views import (
    ListSalesView,
    GetSaleView,
    CreateSaleView,
    UpdateSalesView,
)


app_name = 'sales'

urlpatterns = [
    path('', ListSalesView.as_view(), name='list_sales'),
    path('<int:sale_id>/', GetSaleView.as_view(), name='get_sale'),
    path('create/', CreateSaleView.as_view(), name='create_sale'),
    path('<int:sale_id>/update/', UpdateSalesView.as_view(), name='update_sale'),
]
