from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import csv
import csv

app = Flask(__name__)

# Database setup
DATABASE = 'vocabulary.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database"""
    if not os.path.exists(DATABASE):
        conn = get_db()
        conn.execute('''
            CREATE TABLE words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indonesian TEXT NOT NULL,
                english TEXT NOT NULL
            )
        ''')
        # Add some sample words
        sample_words = [
            ('halo', 'hello'),
            ('terima kasih', 'thank you'),
            ('selamat pagi', 'good morning'),
            ('air', 'water'),
            ('makanan', 'food')
        ]
        conn.executemany('INSERT INTO words (indonesian, english) VALUES (?, ?)', sample_words)
        conn.commit()

        conn.execute('''
            CREATE TABLE phrases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indonesian_phrase TEXT NOT NULL,
                english_phrase TEXT NOT NULL
            )
        ''')
        # Add some sample phrases
        sample_phrases = [
            ('Apa kabar?', 'How are you?'),
            ('Baik-baik saja', 'I am fine'),
            ('Terima kasih banyak', 'Thank you very much'),
            ('Sama-sama', 'You\'re welcome'),
            ('Maaf', 'Sorry')
        ]
        conn.executemany('INSERT INTO phrases (indonesian_phrase, english_phrase) VALUES (?, ?)', sample_phrases)
        conn.commit()
        conn.close()
        conn.close()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/add_word')
def add_word_page():
    """Page to add new words"""
    return render_template('add_word.html')

@app.route('/api/add_word', methods=['POST'])
def add_word():
    """API endpoint to add a new word"""
    data = request.json
    indonesian = data.get('indonesian', '').strip()
    english = data.get('english', '').strip()
    
    if not indonesian or not english:
        return jsonify({'success': False, 'message': 'Both fields are required'}), 400
    
    conn = get_db()
    conn.execute('INSERT INTO words (indonesian, english) VALUES (?, ?)', (indonesian, english))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Word added successfully'})

@app.route('/flashcards')
def flashcards():
    """Flashcards page"""
    return render_template('flashcards.html')

@app.route('/api/words')
def get_words():
    """API endpoint to get all words"""
    conn = get_db()
    cursor = conn.execute('SELECT id, indonesian, english FROM words')
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(words)

@app.route('/api/delete_word/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """API endpoint to delete a word"""
    conn = get_db()
    conn.execute('DELETE FROM words WHERE id = ?', (word_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Word deleted successfully'})

@app.route('/upload_csv')
def upload_csv_page():
    """Page to upload CSV file"""
    return render_template('upload_csv.html')

@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    """API endpoint to upload and process CSV file"""
    if 'csvFile' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['csvFile']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
        
    if file and file.filename.endswith('.csv'):
        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            
            words_to_add = []
            for i, row in enumerate(reader):
                if len(row) == 2:
                    english = row[0].strip()
                    indonesian = row[1].strip()
                    if english and indonesian:
                        words_to_add.append((indonesian, english))
                else:
                    return jsonify({'success': False, 'message': f'Invalid row format at line {i+1}. Expected 2 columns, got {len(row)}'}), 400
            
            if not words_to_add:
                return jsonify({'success': False, 'message': 'No valid words found in CSV'}), 400

            conn = get_db()
            conn.executemany('INSERT INTO words (indonesian, english) VALUES (?, ?)', words_to_add)
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': f'{len(words_to_add)} words added successfully!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'}), 500

    return jsonify({'success': False, 'message': 'Invalid file format. Only CSV files are accepted.'}), 400

@app.route('/phrase_flashcards')
def phrase_flashcards():
    """Phrase flashcards page"""
    return render_template('phrase_flashcards.html')

@app.route('/api/phrases')
def get_phrases():
    """API endpoint to get all phrases"""
    conn = get_db()
    cursor = conn.execute('SELECT id, indonesian_phrase, english_phrase FROM phrases')
    phrases = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(phrases)

@app.route('/manage_phrases')
def manage_phrases_page():
    """Page to add, edit, and delete phrases"""
    return render_template('manage_phrases.html')

@app.route('/api/add_phrase', methods=['POST'])
def add_phrase():
    """API endpoint to add a new phrase"""
    data = request.json
    indonesian_phrase = data.get('indonesian_phrase', '').strip()
    english_phrase = data.get('english_phrase', '').strip()
    
    if not indonesian_phrase or not english_phrase:
        return jsonify({'success': False, 'message': 'Both fields are required'}), 400
    
    conn = get_db()
    conn.execute('INSERT INTO phrases (indonesian_phrase, english_phrase) VALUES (?, ?)', (indonesian_phrase, english_phrase))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Phrase added successfully'})

@app.route('/api/edit_phrase/<int:phrase_id>', methods=['PUT'])
def edit_phrase(phrase_id):
    """API endpoint to edit an existing phrase"""
    data = request.json
    indonesian_phrase = data.get('indonesian_phrase', '').strip()
    english_phrase = data.get('english_phrase', '').strip()
    
    if not indonesian_phrase or not english_phrase:
        return jsonify({'success': False, 'message': 'Both fields are required'}), 400
    
    conn = get_db()
    conn.execute('UPDATE phrases SET indonesian_phrase = ?, english_phrase = ? WHERE id = ?', (indonesian_phrase, english_phrase, phrase_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Phrase updated successfully'})

@app.route('/api/delete_phrase/<int:phrase_id>', methods=['DELETE'])
def delete_phrase(phrase_id):
    """API endpoint to delete a phrase"""
    conn = get_db()
    conn.execute('DELETE FROM phrases WHERE id = ?', (phrase_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Phrase deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5006)
