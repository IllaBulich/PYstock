from django.urls import path, include
from . import views

app_name = 'product'
urlpatterns = [
    path('',views.ProductListView.as_view(), name='main'),
    path('add',views.AddProductView.as_view(), name='add'),
    path('<int:pk>', views.ProductDetailView.as_view(), name = "product_detail"),
    path('<int:pk>/update', views.ProductUpdateView.as_view(),  name = "product_update"),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name = "product_delete"),

]