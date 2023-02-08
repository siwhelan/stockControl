from django.shortcuts import render
import pymongo

# Create your views here.


def stock_control(request):
    # Connect to the MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    ingredients_collection = db["ingredients"]

    # Retrieve all ingredients from the "ingredients" collection
    ingredients = ingredients_collection.find()

    # Initialize an empty list to store the capitalized ingredients
    capitalized_ingredients = []

    # Loop through each ingredient, capitalize each word in the "ingredient" field, and append to the capitalized_ingredients list
    for ingredient in ingredients:
        ingredient['ingredient'] = ingredient['ingredient'].title()
        capitalized_ingredients.append(ingredient)

    # Render the "index.html" template with the capitalized ingredients
    return render(request, 'index.html', {'ingredients': capitalized_ingredients})
