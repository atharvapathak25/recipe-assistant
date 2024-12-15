from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import requests
import openai
from gtts import gTTS
import os
import time

# Initialize Flask app
app = Flask(__name__)

# API Keys
SPOONACULAR_API_KEY = ""  
# Create temp directory for TTS files
if not os.path.exists("temp"):
    os.makedirs("temp")

# Home Route
@app.route('/')
def home():
    # Connect to the database
    connection = sqlite3.connect('recipe_assistant.db')
    cursor = connection.cursor()

    # Get all recipe names from the database
    cursor.execute("SELECT name FROM recipes")
    recipe_names = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Fetch random recipes from Spoonacular API
    try:
        spoonacular_url = "https://api.spoonacular.com/recipes/random"
        params = {"number": 3, "apiKey": SPOONACULAR_API_KEY}
        response = requests.get(spoonacular_url, params=params)

        if response.status_code == 200:
            spoonacular_recipes = response.json().get("recipes", [])
        else:
            spoonacular_recipes = []
    except Exception:
        spoonacular_recipes = []

    # Pass recipe names and Spoonacular recommendations to the template
    return render_template(
        'index.html',
        recipe_names=recipe_names,
        spoonacular_recipes=spoonacular_recipes
    )

# Fetch Recipe Route
@app.route('/fetch_recipe', methods=['POST'])
def fetch_recipe():
    recipe_name = request.form['recipe_name'].strip()
    category = request.form['category']

    # Connect to SQLite database
    connection = sqlite3.connect('recipe_assistant.db')
    cursor = connection.cursor()

    # Query the database based on the provided recipe name and category
    if category:
        cursor.execute("SELECT * FROM recipes WHERE LOWER(name) = LOWER(?) AND category = ?", (recipe_name, category))
    else:
        cursor.execute("SELECT * FROM recipes WHERE LOWER(name) = LOWER(?)", (recipe_name,))

    # Fetch the first matching recipe
    recipe = cursor.fetchone()

    # Close the database connection
    connection.close()

    # Check if a recipe was found
    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    else:
        return "Recipe not found!"

# AI-Generated Recipe Function
def generate_recipe(prompt):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate a recipe using the following ingredients: {prompt}",
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Generate Recipe Route
@app.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    try:
        data = request.json
        prompt = data.get('ingredients', '').strip()
        if not prompt:
            return jsonify({'error': 'No ingredients provided'}), 400
        recipe = generate_recipe(prompt)
        return jsonify({'recipe': recipe})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Text-to-Speech Function
def text_to_speech(text, filename=None):
    if not filename:
        filename = f"response_{int(time.time())}.mp3"
    filepath = os.path.join("temp", filename)
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    return filepath

# Speak Recipe Route
@app.route('/speak-recipe', methods=['POST'])
def speak_recipe():
    try:
        data = request.json
        recipe_text = data.get('recipe', '').strip()
        if not recipe_text:
            return jsonify({'error': 'No recipe provided'}), 400
        audio_file = text_to_speech(recipe_text)
        return jsonify({'audio_file': f'/{audio_file}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download Audio Route
@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    filepath = os.path.join("temp", filename)
    try:
        response = send_from_directory("temp", filename, as_attachment=True)
        os.remove(filepath)
        return response
    except FileNotFoundError:
        return "File not found!", 404

if __name__ == "__main__":
    app.run(debug=True)
