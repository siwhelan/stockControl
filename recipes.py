import pymongo
from scripts import calculate_recipe_costs, add_amounts, delete_amounts


def connect_to_db():
    # Connect to the MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Get the recipes database
    db = client["stock_control"]

    # Get the recipes collection
    recipes_collection = db["recipes"]
    ingredients_collection = db["ingredients"]

    return recipes_collection, ingredients_collection


# Define a class that takes name and ingredients and produces the cost of the recipe
class Recipe:
    # Initialize the Recipe object with a name and a dictionary of ingredients
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

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
        # Connect to the recipes collection
        recipes_collection, ingredients_collection = connect_to_db()

        # Get the code of the last recipe in the database
        last_recipe = recipes_collection.find().sort([("code", -1)]).limit(1)

        if last_recipe is not None:
            # Get the code of the last recipe in the database
            last_recipe = last_recipe[0]
            code = int(last_recipe["code"]) + 1
        else:
            code = 1

        # Format the code to a 5-digit string (e.g. 00001, 00002, etc.)
        recipe_code = str(code).zfill(5)

        # Ask user for recipe name
        recipe_name = input("Enter recipe name: ")
        # Create a dictionary to store ingredients and their amounts
        ingredients = {}
        while True:
            ingredient = input(
                "Enter ingredient name (or enter 'done' when finished): "
            )
            if ingredient.lower() == "done":
                break
            # Check if the ingredient exists in the ingredients collection
            existing_product = ingredients_collection.find_one(
                {"ingredient": ingredient}
            )
            if existing_product:
                # Check if the ingredient amount is a valid integer
                try:
                    amount = int(input(f"Enter amount for {ingredient}: "))
                    ingredients[ingredient] = amount
                except ValueError:
                    print(
                        f"Amount for {ingredient} must be a number. Please try again."
                    )
            else:
                print(
                    f"Ingredient {ingredient} does not exist in the ingredients collection."
                )
                print("Please add the ingredient to the collection first.")
                return  # Abort the recipe creation process

        # Insert the recipe into the recipes collection
        recipe = {
            "name": recipe_name,
            "ingredients": ingredients,
            "code": recipe_code,
        }
        recipes_collection.insert_one(recipe)
        print(f"Successfully added {recipe_name} recipe to the database!")
        calculate_recipe_costs()
        delete_amounts()
        add_amounts()


# Create a new recipe object
recipe = Recipe(
    "cake mix",
    {
        "butter": 175,
        "sugar": 175,
        "eggs": 3,
        "flour": 175,
        "baking powder": 25,
        "vanilla extract": 5,
    },
)

# Call the add_recipe method
recipe.add_recipe()
