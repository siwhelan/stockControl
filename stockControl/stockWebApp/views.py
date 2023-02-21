from .models import Ingredient
from django.contrib import messages
from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.conf import settings
import pymongo

# Create your views here.


def view_ingredients(request):
    # Connect to the MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    ingredients_collection = db["ingredients"]

    # Retrieve all ingredients from the "ingredients" collection
    ingredients = ingredients_collection.find()

    # Initialize an empty list to store the capitalized ingredients
    capitalized_ingredients = []

    # Loop through each ingredient and capitalize each word in the "ingredient" field
    for ingredient in ingredients:
        ingredient["ingredient"] = ingredient["ingredient"].title()
        # Round each price to 2 decimal places
        ingredient["price_per_pack"] = "{:.2f}".format(
            ingredient["price_per_pack"]
        )
        pack_size = ingredient["pack_size"]
        # Round each pack size to 2 decimal places if float
        if int(pack_size) == pack_size:
            pack_size = "{:.0f}".format(pack_size)
        else:
            pack_size = "{:.2f}".format(pack_size)
        ingredient["pack_size"] = pack_size
        # Append to the capitalized_ingredients list
        capitalized_ingredients.append(ingredient)

    # Render the "index.html" template with the capitalized ingredients
    return render(
        request, "view_all_ing.html", {"ingredients": capitalized_ingredients}
    )


def stock_entry(request):

    # Connect to the MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    ingredients_collection = db["ingredients"]

    # Retrieve all ingredients from the "ingredients" collection
    ingredients = ingredients_collection.find()

    # Initialize an empty list to store the capitalized ingredients
    capitalized_ingredients = []

    # Loop through each ingredient and capitalize each word in the "ingredient" field
    for ingredient in ingredients:
        ingredient["ingredient"] = ingredient["ingredient"].title()
        # Round each price to 2 decimal places
        ingredient["price_per_pack"] = "{:.2f}".format(
            ingredient["price_per_pack"]
        )
        pack_size = ingredient["pack_size"]
        # Round each pack size to 2 decimal places if float
        if float(pack_size) == pack_size:
            pack_size = "{:.0f}".format(pack_size)
        else:
            pack_size = "{:.2f}".format(pack_size)
        ingredient["pack_size"] = pack_size
        # Format the amount field in the same way as pack_size
        amount = ingredient["amount"]
        if (amount) == amount:
            amount = "{:.0f}".format(amount)
        else:
            amount = "{:.2f}".format(amount)
        ingredient["amount"] = amount
        # Append to the capitalized_ingredients list
        capitalized_ingredients.append(ingredient)

    # Render the "index.html" template with the capitalized ingredients
    return render(
        request, "stock_entry.html", {"ingredients": capitalized_ingredients}
    )


# View Home Page (currently navbar only)


def home(request):
    return render(request, "base.html")


def add_new_ingredient(request):
    return render(request, "add_new_ingredient.html")


def view_recipe(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    recipes_collection = db["recipes"]

    # Get all recipes from MongoDB
    recipes = recipes_collection.find()

    # Create list of recipe data for rendering in template
    recipe_data = []
    for recipe in recipes:
        recipe_data.append(
            {
                "name": recipe["name"],
                "ingredients": recipe["ingredients"],
                "code": recipe["code"],
                "recipe_cost": recipe["recipe_cost"],
            }
        )

    context = {"recipe_data": recipe_data}
    return render(request, "recipe_card.html", context)


def save_stock_entry(request):
    if request.method == "POST":
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"]

        # Parse form data
        for key, value in request.POST.items():
            if key.startswith("ingredient_") and value != "":
                product_code = key.split("_")[1]
                # convert to float and remove commas
                amount = float(value.replace(",", ""))

                # Update MongoDB document
                ingredients.update_one(
                    {"product_code": product_code},
                    {"$set": {"amount": amount}},
                )

        # Render success message in the same template
        message = "Stock entry saved successfully."
        ingredients = ingredients.find()
        return render(
            request,
            "stock_entry.html",
            {"ingredients": ingredients, "message": message},
        )
    else:
        # Render form page
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"].find()
        return render(
            request, "stock_entry.html", {"ingredients": ingredients}
        )
