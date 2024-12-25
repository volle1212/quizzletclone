from flask import Flask, render_template, request, jsonify, redirect
import json
import random
import string

app = Flask(__name__)
app.config['DEBUG'] = True

# Helper function to load and save flashcards

@app.route('/about')
def about():
    # This route will render the "About Us" page
    return render_template('about.html')

def load_flashcards():
    try:
        with open('flashcards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_random_string(length):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Randomly choose `length` characters from the defined set
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_string(length):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Randomly choose `length` characters from the defined set
    return ''.join(random.choice(characters) for _ in range(length))

# Example usage: 
def save_flashcards(flashcards):
    with open('flashcards.json', 'w') as f:
        json.dump(flashcards, f, indent=4)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/flashcard_generator')
def flashcard_generator():
    return render_template('index.html')

@app.route('/contact')
def contact():
    # Contact Us route
    return render_template('contact.html')

@app.route('/flashcard_generator', methods=['POST'])
def add_flashcard():
    title = request.form.get('title')
    flashcards_data = request.form.get('flashcards')  # Get flashcards as JSON string

    if title and flashcards_data:
        flashcards = load_flashcards()

        # Check if the title already exists
        if title in [fc["title"] for fc in flashcards.values()]:
            return render_template('index.html', 
            message=f"A flashcard set with the title '{title}' already exists. Please choose a different title.", 
            status="error"), 400

        # Parse flashcards
        flashcards_list = json.loads(flashcards_data)

        # Generate a unique code
        code = generate_random_string(15)

        # Add the new flashcard set
        flashcards[code] = {"title": title, "flashcards": flashcards_list}

        # Save the updated flashcards to the file
        save_flashcards(flashcards)
        return render_template('index.html', 
        message="Flashcard set saved successfully!", 
        status="success"), 200

    return render_template('index.html', 
    message="Invalid input. Both title and flashcards are required.", 
    status="error"), 400

@app.route('/view_flashcards', methods=['GET', 'POST'])
def view_flashcards():
    if request.method == 'POST':
        title = request.form.get('title')
        flashcards = load_flashcards()

        # Check if the title exists
        if title in flashcards:
            # Redirect to a GET request with the title as a query parameter
            return redirect(f"/view_flashcards?title={title}")
        else:
            # Redirect with an error message in the query string
            return redirect("/view_flashcards?error=Flashcard set not found.")

    # Handle the GET request
    title = request.args.get('title')
    error = request.args.get('error')
    if title:
        flashcards = load_flashcards()
        if title in flashcards:
            return render_template('view_flashcards.html', title=[0][title]["title"], flashcards=flashcards[title])
    return render_template('view_flashcards.html', error=error)

@app.route('/test_flashcards', methods=['GET', 'POST'])
def test_flashcards():
    flashcards = load_flashcards()

    if request.method == 'POST':
        title = request.form.get('title')
        if title in flashcards:
            return render_template('test_flashcards.html', title=title, flashcards=flashcards[title])
        else:
            return render_template('select_flashcards.html', error="Flashcard set not found.")
    
    # GET request: Render the selection page if no set is selected
    title = request.args.get('title')
    if title and title in flashcards:
        return render_template('test_flashcards.html', title=title, flashcards=flashcards[title])
    return render_template('select_flashcards.html', flashcards=flashcards)


if __name__ == '__main__':
    app.run(debug=True)
