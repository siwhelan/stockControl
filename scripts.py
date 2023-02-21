from pymongo import MongoClient


def add_recipe_codes():
    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    recipes_collection = db["recipes"]

    # Get the current number of recipes
    recipe_count = recipes_collection.count_documents({})

    # Update the code for each recipe in the collection
    for i in range(recipe_count):
        # Get the current recipe
        recipe = recipes_collection.find()[i]

        # Generate the new 5-digit code
        new_code = str(i + 1).zfill(5)

        # Update the recipe with the new code
        recipes_collection.update_one({"_id": recipe["_id"]}, {
                                      "$set": {"code": new_code}})

    print("All recipes have been updated with new codes.")


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
                {"ingredient": ingredient})
            # Calculate the cost of the ingredient by multiplying the quantity needed by the price per pack
            ingredient_cost = quantity * \
                ingredient_info["price_per_pack"] / \
                ingredient_info["pack_size"]
            # Add the cost of the ingredient to the total cost
            cost += ingredient_cost

        # Update the recipe document with the calculated cost
        recipes_collection.update_one({"_id": recipe["_id"]}, {
            "$set": {"recipe_cost": cost}})
        # Print a success message
        print(f"Successfully calculated cost for recipe {recipe['name']}")


def delete_amounts():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_control']
    ingredients = db['ingredients']

    # Update all documents in the collection to remove the "amount" field
    ingredients.update_many({}, {"$unset": {"amount": ""}})


def add_amounts():
    # Connect to the MongoDB database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    collection = db["ingredients"]

    # Loop through all documents in the "ingredients" collection
    for doc in collection.find():
        # Retrieve the current value of "pack_size" for this document
        pack_size = doc["pack_size"]

        # Add the value of "pack_size" to the current amount for this ingredient
        new_amount = doc.get("amount", 0) + pack_size

        # Update the document with the new amount for this ingredient
        collection.update_one({"_id": doc["_id"]}, {
                              "$set": {"amount": new_amount}})

    print("All ingredients have been updated with new amounts.")

