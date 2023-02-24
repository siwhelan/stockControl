from pymongo import MongoClient
from django.shortcuts import render
import pymongo


def home(request):
    return render(request, "base.html")


def view_ingredients(request):
    # Connect to the MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    ingredients_collection = db["ingredients"]

    # Retrieve all ingredients from the "ingredients" collection
    ingredients = ingredients_collection.find()

    # Initialize an empty list to store the capitalized ingredients
    capitalized_ingredients = []

    # Loop through each ingredient and
    # capitalize each word in the "ingredient" field
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


def add_ingredient(request):

    if request.method == "POST":
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"]

        # Get the user input from the form
        ingredient = request.POST.get("ingredient", "")
        price_per_pack = request.POST.get("price_per_pack", "")
        pack_size = request.POST.get("pack_size", "")

        # Check if the ingredient already exists
        existing_ingredient = ingredients.find_one({"ingredient": ingredient})
        if existing_ingredient is not None:
            # If the ingredient already exists, display an error message
            message = "This ingredient already exists."
            alert_type = "danger"
            ingredients = ingredients.find()
            return render(
                request,
                "add_new_ingredient.html",
                {
                    "ingredients": ingredients,
                    "message": message,
                    "alert_type": alert_type,
                },
            )

        # Get the last item in the ingredients database
        last_item = ingredients.find().sort([("product_code", -1)]).limit(1)

        # Check if there are any items in the database
        if last_item is not None:
            # Get the product code of the last item in the database
            last_product_code = last_item[0]["product_code"]

            # Increment code by 1 to get the
            # product code for the new ingredient
            # .zfill(4) adds zeros to the product code
            # so that it is always 4 digits long
            # In the unlikely event that the kitchen
            # uses more than 9999 ingredients,
            # this will need to be changed.
            new_product_code = str(int(last_product_code) + 1).zfill(4)
        else:
            # If there are no items in the database,
            # set the first product code to "0001"
            new_product_code = "0001"

        # Check that the input types are correct
        if (
            isinstance(ingredient, str)
            and isinstance(price_per_pack, str)
            and isinstance(pack_size, str)
        ):
            try:
                # Convert user input to correct data types
                price_per_pack = float(price_per_pack)
                pack_size = int(pack_size)

                # Insert the new ingredient into the database
                ingredients.insert_one(
                    {
                        "product_code": new_product_code,
                        "ingredient": ingredient,
                        "price_per_pack": price_per_pack,
                        "pack_size": pack_size,
                        "amount": pack_size,
                    }
                )

                # Render success message in the
                # add_new_ingredient.html template
                ingredients = ingredients.find()
                message = "New ingredient added successfully."
                alert_type = "success"
                return render(
                    request,
                    "add_new_ingredient.html",
                    {
                        "ingredients": ingredients,
                        "message": message,
                        "alert_type": alert_type,
                    },
                )

            except ValueError:
                # If the conversion fails, display an error message
                message = "Please enter the correct data type for each field."
                alert_type = "danger"
                return render(
                    request,
                    "add_new_ingredient.html",
                    {
                        "ingredients": ingredients,
                        "message": message,
                        "alert_type": alert_type,
                    },
                )

        # If the data types are incorrect, display an error message
        message = "Please enter the correct data type for each field."
        alert_type = "danger"
        return render(
            request,
            "add_new_ingredient.html",
            {
                "ingredients": ingredients,
                "message": message,
                "alert_type": alert_type,
            },
        )

    # If the form has not been submitted, display the page
    return render(request, "add_new_ingredient.html")


def update_ingredient(request):
    if request.method == "POST":
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"]

        # Get the user input from the form
        ingredient = request.POST.get("ingredient", "")
        price_per_pack = request.POST.get("price_per_pack", "")
        pack_size = request.POST.get("pack_size", "")

        # Check if the ingredient exists
        existing_ingredient = ingredients.find_one({"ingredient": ingredient})
        if existing_ingredient is None:
            # If the ingredient doesn't exist, display an error message
            message = "Ingredient not found"
            alert_type = "danger"
            ingredients = ingredients.find()
            return render(
                request,
                "update_ingredient.html",
                {
                    "ingredients": ingredients,
                    "message": message,
                    "alert_type": alert_type,
                },
            )

        # Check that the input types are correct
        if isinstance(price_per_pack, str) and isinstance(pack_size, str):
            try:
                # Convert user input to correct data types
                price_per_pack = (
                    float(price_per_pack) if price_per_pack else None
                )
                pack_size = int(pack_size) if pack_size else None

                # Update MongoDB document
                update_fields = {}
                if price_per_pack is not None:
                    update_fields["price_per_pack"] = price_per_pack
                if pack_size is not None:
                    update_fields["pack_size"] = pack_size

                if update_fields:
                    ingredients.update_one(
                        {"ingredient": ingredient},
                        {"$set": update_fields},
                    )

                # Render success message in the update_ingredient.html template
                ingredients = ingredients.find()
                message = "Ingredient updated successfully."
                alert_type = "success"
                return render(
                    request,
                    "update_ingredient.html",
                    {
                        "ingredients": ingredients,
                        "message": message,
                        "alert_type": alert_type,
                    },
                )

            except ValueError:
                # If the conversion fails, display an error message
                message = "Please enter the correct data type for each field."
                alert_type = "danger"
                ingredients = ingredients.find()
                return render(
                    request,
                    "update_ingredient.html",
                    {
                        "ingredients": ingredients,
                        "message": message,
                        "alert_type": alert_type,
                    },
                )

        # If the data types are incorrect, display an error message
        message = "Please enter the correct data type for each field."
        alert_type = "danger"
        ingredients = ingredients.find()
        return render(
            request,
            "update_ingredient.html",
            {
                "ingredients": ingredients,
                "message": message,
                "alert_type": alert_type,
            },
        )

    # If the form has not been submitted, display the page
    return render(request, "update_ingredient.html")


def delete_ingredient(request):
    if request.method == "POST":
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"]

        # Get the user input from the form
        ingredient = request.POST.get("ingredient", "")

        # Check if the ingredient exists
        existing_ingredient = ingredients.find_one({"ingredient": ingredient})
        if existing_ingredient is None:
            # If the ingredient doesn't exist, display an error message
            message = "Ingredient not found"
            alert_type = "danger"
            ingredients = ingredients.find()
            return render(
                request,
                "delete_ingredient.html",
                {
                    "ingredients": ingredients,
                    "message": message,
                    "alert_type": alert_type,
                },
            )
        else:
            # Delete the ingredient
            ingredients.delete_one({"ingredient": ingredient})
            # Render success message in the update_ingredient.html template
            ingredients = ingredients.find()
            message = "Ingredient deleted successfully."
            alert_type = "success"
            return render(
                request,
                "delete_ingredient.html",
                {
                    "ingredients": ingredients,
                    "message": message,
                    "alert_type": alert_type,
                },
            )
    # If the form has not been submitted, display the page
    return render(request, "delete_ingredient.html")


def calculate_recipe_costs():
    # Connect to the MongoDB client
    client = MongoClient("mongodb://localhost:27017/")
    # Select the "stock_control" database
    db = client["stock_control"]
    # Select the "recipes" collection
    recipes_collection = db["recipes"]
    # Select the "ingredients" collection
    ingredients_collection = db["ingredients"]
    # Find all recipe documents in the database
    recipes = recipes_collection.find()
    # Loop through each recipe
    for recipe in recipes:
        # Calculate the cost of the recipe
        cost = 0
        # Loop through each ingredient in the recipe
        for ingredient, quantity in recipe["ingredients"].items():
            # Retrieve the information for the current ingredient from the ingredients collection
            ingredient_info = ingredients_collection.find_one(
                {"ingredient": ingredient}
            )
            # Calculate the cost of the ingredient by multiplying the quantity needed by the price per pack
            ingredient_cost = (
                quantity
                * ingredient_info["price_per_pack"]
                / ingredient_info["pack_size"]
            )
            # Add the cost of the ingredient to the total cost
            cost += ingredient_cost

        # Update the recipe document with the calculated cost
        recipes_collection.update_one(
            {"_id": recipe["_id"]}, {"$set": {"recipe_cost": cost}}
        )
        # Print a success message
        print(f"Successfully calculated cost for recipe {recipe['name']}")


def view_recipe(request):

    calculate_recipe_costs()
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


def add_recipe(request):
    return render(request, "add_recipe.html")


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


def wastage(request):

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
                amount = -float(
                    value.replace(",", "")
                )  # negative value for reduction

                # Update MongoDB document by reducing the existing amount
                ingredients.update_one(
                    {"product_code": product_code},
                    {"$inc": {"amount": amount}},
                )

        # Render success message in the same template
        message = "Wastage recorded and stock updated ."
        ingredients = ingredients.find()
        return render(
            request,
            "wastage.html",
            {"ingredients": ingredients, "message": message},
        )
    else:
        # Render form page
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"].find()
        return render(request, "wastage.html", {"ingredients": ingredients})


def orders(request):

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

                # Update MongoDB document by adding the
                # ordered amount to the the existing one.
                ingredients.update_one(
                    {"product_code": product_code},
                    {"$inc": {"amount": amount}},
                )

        # Render success message in the same template
        message = "Orders placed with your suppliers."
        ingredients = ingredients.find()
        return render(
            request,
            "place_orders.html",
            {"ingredients": ingredients, "message": message},
        )
    else:
        # Render form page
        client = MongoClient("mongodb://localhost:27017/")
        db = client["stock_control"]
        ingredients = db["ingredients"].find()
        return render(
            request, "place_orders.html", {"ingredients": ingredients}
        )
