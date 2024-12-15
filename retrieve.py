import sqlite3

# Connect to the database
connection = sqlite3.connect("recipe_assistant.db")
cursor = connection.cursor()

# Fetch all recipes
cursor.execute("SELECT * FROM recipes")
recipes = cursor.fetchall()

for recipe in recipes:
    print(f"ID: {recipe[0]}, Name: {recipe[1]}, Category: {recipe[4]}")
    print(f"Ingredients: {recipe[2]}")
    print(f"Instructions: {recipe[3]}")
    print(f"Health Tag: {recipe[5]}\n")

connection.close()
