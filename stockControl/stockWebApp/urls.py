from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ingredients/view/", views.view_ingredients, name="view_ingredients"),
    path("ingredients/new/", views.add_ingredient, name="add_ingredient"),
    path("stock_entry/", views.save_stock_entry, name="save_stock_entry"),
    path("orders/", views.orders, name="orders"),
    path("wastage/", views.wastage, name="wastage"),
    path(
        "ingredients/update/",
        views.update_ingredient,
        name="update_ingredient",
    ),
    path(
        "ingredients/delete/",
        views.delete_ingredient,
        name="delete_ingredient",
    ),
    path("recipes/view/", views.view_recipe, name="view_recipe"),
    path("recipes/new/", views.add_recipe, name="add_recipe"),
]
