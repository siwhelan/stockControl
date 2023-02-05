import pymongo
from ingredients import ingredients

def connect_to_db():
    # Connect to the MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    # Get the recipes database
    db = client["stock_control"]
    
    # Get the recipes collection
    recipes_collection = db["recipes"]
    ingredients_collection = db["ingredients"]

    
    
    return recipes_collection


# Define a class that takes name and ingredients and produces the cost of the recipe
class Recipe:
    # Initialize the Recipe object with a name and a dictionary of ingredients
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    # Calculate the total cost of the recipe by summing up the cost per gram of each ingredient
    def total_cost(self):
        total = 0
        for ingredient, amount in self.ingredients.items():
            # Find the Item object in the ingredients list that corresponds to this ingredient
            item = next((x for x in ingredients if x.ingredient == ingredient), None)
            if item:
                # Calculate the cost of this ingredient by multiplying its cost per gram by the amount in grams
                total += item.price_per_gram() * amount
        return total

    # Define a string representation of the Recipe object
    def __str__(self):
        # Create a string representation of each ingredient in the form "ingredient (amount)g"
        ingredients_str = ", ".join(
            [
                f"{ingredient} ({amount}g)"
                for ingredient, amount in self.ingredients.items()
            ]
        )
        return f"{self.name}: {ingredients_str}"

    def add_recipe(self):
        pass