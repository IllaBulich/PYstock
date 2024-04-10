
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='warehouses/main'),
    path('add', views.AddStockView.as_view(), name='warehouses/add'),
    path('<int:pk>', views.StockDetailView.as_view(),  name = "warehouses/stock_detail"),
    path('<int:pk>/update', views.StockUpdateView.as_view(), name = "warehouses/stock_update"),
    path('<int:pk>/delete', views.StockDeleteView.as_view(), name = "warehouses/stock_delete"),  
    
]