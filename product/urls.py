from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(), name='product/main'),
    path('add',views.AddProductView.as_view(), name='product/add'),
    path('<int:pk>', views.ProductDetailView.as_view(), name = "product/product_detail"),
    path('<int:pk>/update', views.ProductUpdateView.as_view(),  name = "product/product_update"),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name = "product/product_delete"),


    path('add_item', views.AddItemView.as_view(), name='item/add_item'),
#     path('delete_item/<int:item_id>/', views.delete_item, name='item/delete_item'),
    path('sales_item', views.ItemListView.as_view(), name='item/sales_item'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name = "item/item_detail"),
    path('item/<int:pk>/update', views.ItemUpdateView.as_view(), name = "item/item_update"),
   

]