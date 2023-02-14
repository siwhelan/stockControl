from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingredients/view/', views.view_ingredients, name='view_ingredients'),
    path('stocktake', views.stocktake, name='stocktake'),
    path('viewrecipe', views.view_recipe, name="view_recipe"),
]
