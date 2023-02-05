import pymongo

# Define a class named item that takes:
# name, price per pack, pack size in grams


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


def new_ingredient():
    # Connect to the ingredients database
    collection = connect_to_ingredients_db()

    # Get the last item in the ingredients database
    last_item = collection.find().sort([("product_code", -1)]).limit(1)

    # Check if there are any items in the database
    if last_item is not None:
        # Get the product code of the last item in the database
        last_product_code = last_item[0]["product_code"]

        # Increment code by 1 to get the product code for the new ingredient
        # .zfill(4) adds zeros to the product code so that it is always 4 digits long
        # In the unlikely event that the kitchen uses more than 9999 ingredients,
        # this will need to be changed
        new_product_code = str(int(last_product_code) + 1).zfill(4)
    else:
        # If there are no items in the database, 
        # set the first product code to "0001"
        new_product_code = "0001"

    # Get the name of the new ingredient from the user
    ingredient_name = input("What is the name of the ingredient? ")

    # Check if the product already exists in the collection
    existing_product = collection.find_one({"ingredient": ingredient_name})

    if existing_product:
        print("Product already exists in the collection.")

    else:
        # Get the price per pack and pack size from the user
        price_per_pack = float(input("What is the price per pack? "))
        pack_size = float(input("What is the pack size in grams? "))

        # Create a new item object with the given information
        new_item = Item(
            new_product_code, ingredient_name, price_per_pack, pack_size
        )

        # Add the new item to the ingredients collection in MongoDB
        connect_to_ingredients_db().insert_one(new_item.__dict__)

        # Print confirmation to the user
        print(
            f"Item '{ingredient_name}' has been added to the list with product code '{new_product_code}'."
        )


def update_ingredient():
    # Get the product code of the ingredient to update
    product_code = input(
        "Enter the product code of the ingredient to update: "
    )

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
    product_code = input(
        "Enter the product code of the ingredient to delete: "
    )

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
