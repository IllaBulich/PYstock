
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.view_func, name='view_func'),
    path('',views.FuncView.as_view(), name='view_func'),
    path('sales',views.SalesView.as_view(), name='view_sales'),
    path('mixed',views.MixedView.as_view(), name='view_mixed'),
    path('1',views.demand_forecast, name='demand_forecast'),
    
]