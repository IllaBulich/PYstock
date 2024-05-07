
from django.urls import path, include
from . import views

app_name = 'warehouses'
urlpatterns = [
    path('', views.StockListView.as_view(), name='main'),
    path('add', views.AddStockView.as_view(), name='add'),
    path('<int:pk>', views.StockDetailView.as_view(),  name = "stock_detail"),
    path('<int:pk>/update', views.StockUpdateView.as_view(), name = "stock_update"),
    path('<int:pk>/delete', views.StockDeleteView.as_view(), name = "stock_delete"),  
    
]