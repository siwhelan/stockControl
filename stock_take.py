
from pymongo import MongoClient


def stock_entry(ingredients, amounts):
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')
    # Access the stock_control database
    db = client['stock_control']
    # Access the ingredients collection
    collection = db['ingredients']

    # Iterate through each ingredient and its corresponding amount
    for i, amount in enumerate(amounts):
        # Get the current ingredient from the ingredients list
        ingredient = ingredients[i]
        # Find the document in the ingredients collection that matches the current ingredient
        doc = collection.find_one({'ingredient': ingredient})
        # If the document exists
        if doc:
            # Get the current amount of the ingredient from the document
            current_amount = doc['amount']
            # Calculate the new amount of the ingredient after updating it
            new_amount = current_amount + int(amount)
            # If the new amount is less than zero, set it to zero
            if new_amount < 0:
                new_amount = 0
            # Update the document with the new amount of the ingredient
            collection.update_one({'ingredient': ingredient}, {
                                  '$set': {'amount': new_amount}})
        else:
            # If the document doesn't exist, create a new document for the current ingredient
            collection.insert_one(
                {'ingredient': ingredient, 'amount': int(amount)})
