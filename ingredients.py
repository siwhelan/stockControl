import pymongo

# Define a class named item that takes name, ingredients, price per pack, pack size in grams, price per gram


class Item:
    def __init__(self, product_code, ingredient, price_per_pack, pack_size):
        self.product_code = product_code
        self.ingredient = ingredient
        self.price_per_pack = price_per_pack
        self.pack_size = pack_size

    def __str__(self):
        return f"{self.product_code}, {self.ingredient}, {self.price_per_pack}, {self.pack_size}"

    def price_per_gram(self):
        return self.price_per_pack / self.pack_size


def connect_to_ingredients_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock_control"]
    collection = db["ingredients"]
    return collection


ingredients = [
    Item("0001", "paprika", 4.99, 50),
    Item("0002", "sugar", 1.99, 1000),
    Item("0003", "flour", 2.99, 1000),
    Item("0004", "salt", 0.99, 1000),
    Item("0005", "oregano", 2.49, 25),
    Item("0006", "basil", 2.99, 25),
    Item("0007", "cumin", 3.49, 25),
    Item("0008", "coriander", 2.99, 25),
    Item("0009", "turmeric", 3.99, 25),
    Item("0010", "cinnamon", 1.99, 50),
    Item("0011", "ginger", 3.49, 50),
    Item("0012", "cloves", 4.99, 10),
    Item("0013", "nutmeg", 3.99, 10),
    Item("0014", "allspice", 1.99, 25),
    Item("0015", "vanilla extract", 3.99, 50),
    Item("0016", "baking powder", 0.99, 100),
    Item("0017", "baking soda", 0.79, 100),
    Item("0018", "yeast", 1.49, 100),
    Item("0019", "butter", 1.99, 250),
    Item("0020", "olive oil", 2.99, 500),
    Item("0021", "vegetable oil", 1.49, 500),
    Item("0022", "milk", 0.99, 1000),
    Item("0023", "eggs", 1.49, 6),
    Item("0024", "cheddar cheese", 2.49, 200),
    Item("0025", "parmesan cheese", 3.49, 100),
    Item("0026", "mozzarella cheese", 2.99, 200),
    Item("0027", "cream cheese", 1.99, 250),
    Item("0028", "mayonnaise", 1.99, 500),
    Item("0029", "mustard", 0.99, 200),
    Item("0030", "ketchup", 0.99, 500),
    Item("0030", "beef", 5.99, 500),
    Item("0031", "chicken", 4.99, 500),
    Item("0032", "pork", 6.99, 500),
    Item("0033", "lamb", 7.99, 500),
    Item("0034", "salmon", 8.99, 250),
    Item("0035", "tuna", 2.99, 200),
    Item("0036", "prawn", 6.99, 250),
    Item("0037", "scallops", 8.99, 200),
    Item("0038", "onions", 0.99, 500),
    Item("0039", "carrots", 0.99, 500),
    Item("0040", "potatoes", 1.99, 1000),
    Item("0041", "broccoli", 2.99, 500),
    Item("0042", "cauliflower", 2.99, 500),
    Item("0043", "mushrooms", 2.49, 250),
    Item("0044", "peppers", 2.49, 500),
    Item("0045", "spinach", 2.99, 500),
    Item("0046", "kale", 2.99, 500),
    Item("0047", "cucumber", 0.99, 500),
    Item("0048", "tomatoes", 1.99, 500),
    Item("0049", "garlic", 0.99, 50),
    Item("0050", "ginger", 1.99, 100),
]


def new_ingredient():
    # Get the product code of the last item in the ingredients list
    product_code = ingredients[-1].product_code

    # Increment the product code by 1 to get the product code for the new ingredient
    new_product_code = str(int(product_code) + 1).zfill(4)

    # Get the name of the new ingredient from the user
    ingredient_name = input("What is the name of the ingredient? ")

    # Connect to the ingredients database
    collection = connect_to_ingredients_db()

    # Check if the product already exists in the collection
    existing_product = collection.find_one({"ingredient": ingredient_name})

    if existing_product:
        print("Product already exists in the collection.")

    else:
        # Get the price per pack and pack size from the user
        price_per_pack = float(input("What is the price per pack? "))
        pack_size = float(input("What is the pack size in grams? "))

        # Create a new item object with the given information
        new_item = Item(new_product_code, ingredient_name, price_per_pack, pack_size)

        # Add the new item to the ingredients collection in MongoDB
        connect_to_ingredients_db().insert_one(new_item.__dict__)

        # Print confirmation to the user
        print(
            f"Item '{ingredient_name}' has been added to the list with product code '{new_product_code}'."
        )


def update_ingredient():
    # Get the product code of the ingredient to update
    product_code = input("Enter the product code of the ingredient to update: ")

    # Connect to the ingredients database
    collection = connect_to_ingredients_db()

    # Check if the ingredient exists in the collection
    ingredient_data = collection.find_one({"product_code": product_code})
    if ingredient_data is None:
        print("Ingredient not found.")
        return

    # Get the updated information for the ingredient
    # Allow skipping of fields by pressing enter
    ingredient = input(
        "Enter the updated name of the ingredient (press enter to skip): "
    ) or ingredient_data.get("ingredient")
    price_per_pack = float(
        input(
            "Enter the updated price per pack of the ingredient (press enter to skip): "
        )
        or ingredient_data.get("price_per_pack")
    )
    pack_size = float(
        input(
            "Enter the updated pack size in grams of the ingredient (press enter to skip): "
        )
        or ingredient_data.get("pack_size")
    )

    # Update the ingredient in the ingredients list
    for i in range(len(ingredients)):
        if ingredients[i].product_code == product_code:
            ingredients[i].ingredient = ingredient
            ingredients[i].price_per_pack = price_per_pack
            ingredients[i].pack_size = pack_size

    # Update the ingredient in the ingredients collection
    collection.update_one(
        {"product_code": product_code},
        {
            "$set": {
                "ingredient": ingredient,
                "price_per_pack": price_per_pack,
                "pack_size": pack_size,
            }
        },
    )
    print("Ingredient updated successfully!")


# update_ingredient()


def delete_ingredient():

    # Get the product code of the ingredient to delete
    product_code = input("Enter the product code of the ingredient to delete: ")

    # Connect to the ingredients database
    collection = connect_to_ingredients_db()

    # Check if the product exists in the collection
    existing_product = collection.find_one({"product_code": product_code})

    if not existing_product:
        print("Product does not exist in the collection.")

    else:
        # Delete the product from the collection
        connect_to_ingredients_db().delete_one({"product_code": product_code})
        print("Ingredient deleted successfully!")


# delete_ingredient()
