from flask import Flask, render_template, request, jsonify
import sqlite3
import os

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5006)
