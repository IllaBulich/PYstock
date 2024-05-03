
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.view_func, name='view_func'),
    path('',views.FuncView.as_view(), name='view_func'),
    path('sales',views.SalesView.as_view(), name='view_sales'),
    path('mixed',views.MixedView.as_view(), name='view_mixed'),
    path('demand_forecast',views.DemandForecastView.as_view(), name='demand_forecast'),
    
    
]