import sqlite3
connection = sqlite3.connect("recipe_assistant.db")
cursor = connection.cursor()

recipe_name = input("Enter the recipe name: ")

cursor.execute("SELECT * FROM recipes WHERE name = ?", (recipe_name,))
recipe = cursor.fetchone()

if recipe:
    print(f"Recipe Name: {recipe[1]}")
    print(f"Ingredients: {recipe[2]}")
    print(f"Instructions: {recipe[3]}")
    print(f"Category: {recipe[4]}")
    print(f"Health Tag: {recipe[5]}")
else:
    print("Recipe not found!")

connection.close()
