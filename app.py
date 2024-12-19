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

@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    print(generate_random_string(15))
    title = request.form.get('title')
    text = request.form.get('text')

    if title and text:
        flashcards = load_flashcards()

        # Check if the title already exists
        if title in flashcards:
            return jsonify({"message": f"A flashcard set with the title '{title}' already exists. Please choose a different title."}), 400

        # Create a new set of flashcards
        flashcard_entries = text.split('\n')
        flashcard_set = []

        for entry in flashcard_entries:
            parts = entry.split(' = ')
            if len(parts) == 2:
                question, answer = parts
                flashcard_set.append({"question": question.strip(), "answer": answer.strip()})

        # Add the new set under the provided title
        flashcards[title] = flashcard_set

        # Save the updated flashcards to the file
        save_flashcards(flashcards)
        return jsonify({"message": "Flashcard set saved successfully!"}), 200

    return jsonify({"message": "Invalid input. Both title and flashcards are required."}), 400

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
            return render_template('view_flashcards.html', title=title, flashcards=flashcards[title])
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
