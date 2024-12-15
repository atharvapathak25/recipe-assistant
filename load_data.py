import csv
import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('recipe_assistant.db')
cursor = connection.cursor()

# Create the table (if not already created)
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    category TEXT NOT NULL,
    health_tag TEXT
)
''')

# Open the CSV file with UTF-8 encoding
with open('recipes.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    
    for row in csv_reader:
        # Insert data into the recipes table
        cursor.execute('''
            INSERT INTO recipes (name, ingredients, instructions, category, health_tag)
            VALUES (?, ?, ?, ?, ?)
        ''', (row[0], row[1], row[2], row[3], row[4]))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Data loaded successfully!")
