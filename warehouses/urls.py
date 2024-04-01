
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.main, name='warehouses/main'),
    path('add',views.add, name='warehouses/add'),
    path('<id>', views.stock_detail,  name = "warehouses/stock_detail"),
    path('<int:pk>/update',
         views.StockUpdateView.as_view(), 
         name = "warehouses/stock_update"),
    path('<int:pk>/delete',
         views.StockDeleteView.as_view(), 
         name = "warehouses/stock_delete"),  
    
]