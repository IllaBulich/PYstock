from django.urls import path, include
from . import views

app_name = 'item'
urlpatterns = [
    path('add_item', views.AddItemView.as_view(), name='add_item'),
#     path('delete_item/<int:item_id>/', views.delete_item, name='item/delete_item'),
    path('sales_item', views.ItemListView.as_view(), name='sales_item'),
    path('<int:pk>', views.ItemDetailView.as_view(), name = "item_detail"),
    path('<int:pk>/update', views.ItemUpdateView.as_view(), name = "item_update"),
    path('generate_qr_code/<int:item_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('upload_qr_code', views.upload_qr_code, name='upload_qr_code'),
   
    path('sales/<int:pk>', views.SalesItemDetailView.as_view(), name = "sales_item_detail"),

]