from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.main, name='product/main'),
    path('add',views.add, name='product/add'),
    path('<int:pk>', 
         views.ProductDetailView.as_view(), 
         name = "product/product_detail"),
    path('<int:pk>/update',
         views.ProductUpdateView.as_view(), 
         name = "product/product_update"),
    path('<int:pk>/delete',
         views.ProductDeleteView.as_view(), 
         name = "product/product_delete"),
     
    path('add_item',views.add_item, name='product/add_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='product/delete_item'),
    path('sales_item',views.ItemListView.as_view(), name='product/sales_item'),
   

]