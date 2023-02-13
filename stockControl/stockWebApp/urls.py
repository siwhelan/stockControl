from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.stock_control, name='stock_control'),
    path('stocktake', views.stocktake, name='stocktake')
]
