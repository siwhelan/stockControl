from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.index),
    path('', views.stock_control, name='stock_control'),
]