import sqlite3
import openai

# Database Operations
def insert_sample_data():
    """Insert sample data into the SQLite database."""
    connection = sqlite3.connect("recipe_assistant.db")
    cursor = connection.cursor()

    # Create the `recipes` table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL,
        category TEXT NOT NULL,
        health_tag TEXT NOT NULL
    )
    ''')

    # Insert sample recipes
    cursor.execute('''
    INSERT INTO recipes (name, ingredients, instructions, category, health_tag) 
    VALUES (
        'Paneer Butter Masala', 
        'Paneer: 250g, Butter: 2 tbsp, Tomato: 3', 
        '1. Saute onions and tomatoes. 2. Add paneer and cook.', 
        'VEG', 
        'Healthy'
    )
    ''')

    cursor.execute('''
    INSERT INTO recipes (name, ingredients, instructions, category, health_tag) 
    VALUES (
        'Chicken Curry', 
        'Chicken: 500g, Onion: 2, Garlic: 5 cloves', 
        '1. Marinate chicken. 2. Cook with spices.', 
        'NON-VEG', 
        'Unhealthy'
    )
    ''')

    print("Sample data inserted successfully!")
    connection.commit()
    connection.close()

# AI Recipe Generator
def generate_recipe(prompt):
    """
    Generate a recipe based on the provided ingredients using OpenAI's GPT model.
    Args:
        prompt (str): Ingredients list or description.
    Returns:
        str: Generated recipe.
    """
    openai.api_key = "your-api-key"  # Replace with your OpenAI API key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate a recipe using: {prompt}",
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in generating recipe: {str(e)}"

# Debugging and Testing
if __name__ == "__main__":
    # Uncomment to insert sample data into the database
    # insert_sample_data()

    # Test AI recipe generation
    test_ingredients = "potatoes, peas, and spices"
    generated_recipe = generate_recipe(test_ingredients)
    print("Generated Recipe:")
    print(generated_recipe)
