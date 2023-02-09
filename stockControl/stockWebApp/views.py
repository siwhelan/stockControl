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

    # Loop through each ingredient and capitalize each word in the "ingredient" field
    for ingredient in ingredients:
        ingredient['ingredient'] = ingredient['ingredient'].title()
        # Round each price to 2 decimal places
        ingredient['price_per_pack'] = "{:.2f}".format(ingredient['price_per_pack'])
        pack_size = ingredient['pack_size']
        # Round each pack size to 2 decimal places if float
        if int(pack_size) == pack_size:
            pack_size = "{:.0f}".format(pack_size)
        else:
            pack_size = "{:.2f}".format(pack_size)
        ingredient['pack_size'] = pack_size
        # Append to the capitalized_ingredients list
        capitalized_ingredients.append(ingredient)


    # Render the "index.html" template with the capitalized ingredients
    return render(request, 'index.html', {'ingredients': capitalized_ingredients})

