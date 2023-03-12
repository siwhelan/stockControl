# stockControl 🥕🥫🦐

A Django web app designed to streamline a commercial catering facility's operations with features for stock control, recipe creation and costing, gross profit guidance, and more.

With the aim of providing a complete food management system, this project leverages my experience in the hospitality industry to offer a user-friendly solution for monitoring food costs and kitchen management.

## 🎥 Video Demo -> <a href="https://www.youtube.com/watch?v=a4n57JMSNXU" target="_blank">Link</a>


The main features are -

## 🍅 Ingredients -

#### View / Add / Edit / Delete

Ingredients are stored with name, pack size (weight) and price per pack. A four digit reference code is auto assigned upon entry to the database. An amount is stored that is defaulted to match the pack size to simulate the current stock level of each ingredient.

## 🍴 Recipes -

#### View / Add / Edit / Delete

Recipes are stored with name, ingredients list with amounts, and a five digit auto-assigned reference code. A cost is calculated using the prices of each Ingredient in the relative database collection, and a recommended selling price is added by calculating a 75% Gross Profit margin based on the full cost of each recipe. These details are all displayed in the recipe card view.

## 📦 Stock Entry -

This allows the user to enter the current stock levels they have on site. The ingredient amount is updated to reflect this amount upon entry.

## 🛍️ Ordering -

This allows the user to simulate ordering items from a supplier. The ordered ingredient amount is increased to include the new stock.

## 🗑️ Wastage -

This allows the entry of any items that have been wasted. The current stock holding of each ingredient is reduced to reflect entered amounts.

## 💰 Sales -

This displays all recipes in the database and allows the user to input the number of each that has been sold. This then returns a total revenue figure calculated from the selling price of each recipe, and reduces the stock amount of each ingredient in the recipes sold.

## 🔍 Recipe search - 

Allows searching by recipe code or name. The user can also search for a particular ingredient, which then displays the recipe cards of all recipes that contain it.

## 📝 Blog series - https://lnkd.in/eewznxnD
<br>
Feedback is welcome and appreciated! 👋
