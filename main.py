from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Helper function to load and save flashcards
def load_flashcards():
    try:
        with open('flashcards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_flashcards(flashcards):
    with open('flashcards.json', 'w') as f:
        json.dump(flashcards, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    title = request.form.get('title')
    text = request.form.get('text')
    
    if title and text:
        flashcards = load_flashcards()

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

@app.route('/take_test', methods=['GET', 'POST'])
def take_test():
    if request.method == 'POST':
        title = request.form.get('title')
        flashcards = load_flashcards()

        # Create a case-insensitive mapping from lowercase titles to original titles
        flashcards_lower = {key.lower(): key for key in flashcards}

        # Check if the title exists
        title_lower = title.lower()
        if title_lower in flashcards_lower:
            # Get the original case-sensitive title
            original_title = flashcards_lower[title_lower]
            flashcard_set = flashcards[original_title]

            # Compare answers for each flashcard
            results = []
            for index, flashcard in enumerate(flashcard_set):
                user_answer = request.form.get(f'answer-{index}')
                correct_answer = flashcard['answer']
                is_correct = user_answer.strip().lower() == correct_answer.lower()
                results.append({
                    'question': flashcard['question'],
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct
                })

            return render_template('test_results.html', title=original_title, results=results)

        else:
            return render_template('take_test.html', error="Flashcard set not found.")

    return render_template('take_test.html')

if __name__ == '__main__':
    app.run(debug=True)
