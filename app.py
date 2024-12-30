from flask import Flask, render_template, request, jsonify, redirect
import json
import random
import string
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def homepage():
    # This route will render the "About Us" page
    return render_template('homepage.html')

@app.route('/ämnen')
def subjects():
    # This route will render the "About Us" page
    return render_template('subjects.html')


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

########################################################################
def generate_random_string(length=15):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Randomly choose `length` characters from the defined set
    return ''.join(random.choice(characters) for _ in range(length))

def load_flashcards():
    """Load existing flashcards from the json file."""
    if os.path.exists('flashcards.json'):
        with open('flashcards.json', 'r') as json_file:
            return json.load(json_file)
    return {}

@app.route('/flashcard_generator', methods=['GET', 'POST'])
def flashcard_generator():
    if request.method == 'POST':
        # Handle saving flashcards
        title = request.json.get('title')
        flashcards = request.json.get('flashcards')

        # Generate a random 15-character code
        random_code = generate_random_string()

        # Wrap the flashcard data inside the random code
        flashcard_data = {
            random_code: {
                'title': title,
                'flashcards': flashcards
            }
        }

        # Load existing flashcards from the JSON file
        existing_data = load_flashcards()

        # Append the new flashcard data to the existing data
        existing_data.update(flashcard_data)

        # Save the updated data back to flashcards.json
        try:
            with open('flashcards.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            print(flashcard_data)

            return jsonify({'message': 'Flashcards saved successfully!', 'data': flashcard_data})

        except Exception as e:
            return jsonify({'message': f'Error saving flashcards: {str(e)}'}), 500

    # Handle rendering the form on GET request
    return render_template('index.html')
########################################################################

@app.route('/contact')
def contact():
    # Contact Us route
    return render_template('contact.html')

##########################################################################
@app.route('/view_flashcards', methods=['GET', 'POST'])
def search_flashcards():
    flashcards_data = load_flashcards()
    flashcards = None
    if request.method == 'POST':
        code = request.form.get('code')
        flashcards = flashcards_data.get(code)
    return render_template('view_flashcards.html', flashcards=flashcards)
#############################################################################
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

@app.route('/So', methods=['GET', 'POST'])
def So():
    flashcards_data = load_flashcards()
    flashcards = None
    code = "rnEcBFbSEdHYGUj"
    flashcards = flashcards_data.get(code)
    return render_template('So.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(debug=True)
