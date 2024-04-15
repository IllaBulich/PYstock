
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.view_func, name='view_func'),
    path('',views.FuncView.as_view(), name='view_func'),
    path('2',views.SalesView.as_view()),
    path('1',views.demand_forecast, name='demand_forecast'),
    
]