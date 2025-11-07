# Bahasa Indonesian Flashcards Web App

A simple, interactive web application for learning Bahasa Indonesian and English vocabulary using flashcards.

## Features

- **Add Words**: Easily add Indonesian-English word pairs to your vocabulary
- **Interactive Flashcards**: Practice with a quiz-style flashcard system
- **Two-Way Learning**: Choose to practice Indonesian → English or English → Indonesian
- **Second Chance System**: Get two attempts to answer correctly before seeing the correct answer
- **Visual Feedback**: Green check marks for correct answers, red crosses for incorrect ones
- **Progress Tracking**: See your accuracy and score at the end of each session
- **Pre-loaded Sample Words**: Start practicing immediately with built-in sample vocabulary

## Installation

1. Make sure you have Python 3.7+ installed on your system

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. You're ready to start learning!

## How to Use

### Adding Words

1. Click "Add Words" from the home page
2. Enter an Indonesian word and its English meaning
3. Click "Add Word" to save it to your vocabulary
4. View, manage, and delete words from the word list below

### Practicing with Flashcards

1. Click "Start Practice" from the home page
2. Choose your practice mode:
   - **Practice Indonesian**: You'll see Indonesian words and type English meanings
   - **Practice English**: You'll see English words and type Indonesian meanings
3. Type your answer and press Enter or click Submit
4. You get two attempts per word:
   - Correct on first or second try: Green tick ✅
   - Wrong after two tries: Red cross ❌ + correct answer shown
5. Click "Next Card" to continue
6. View your results at the end with accuracy statistics

## Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── vocabulary.db          # SQLite database (created automatically)
├── templates/
│   ├── index.html         # Home page
│   ├── add_word.html      # Add words page
│   └── flashcards.html    # Quiz page
└── static/
    ├── style.css          # Styling
    └── flashcards.js      # Quiz functionality
```

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradient backgrounds

## Sample Words Included

The application comes with 5 pre-loaded word pairs:
- halo → hello
- terima kasih → thank you
- selamat pagi → good morning
- air → water
- makanan → food

## Notes

- No login required - simple and straightforward to use
- Words are stored locally in an SQLite database
- The database is created automatically on first run
- All answers are case-insensitive for easier learning

## Customization

You can easily customize:
- Colors in `static/style.css`
- Sample words in the `init_db()` function in `app.py`
- Number of attempts per word in `static/flashcards.js`

## Troubleshooting

**Problem**: Application won't start
- Make sure Flask is installed: `pip install Flask`
- Check that port 5000 is not in use by another application

**Problem**: Database errors
- Delete `vocabulary.db` and restart the app to recreate it

**Problem**: Can't add words
- Check browser console for errors
- Ensure both fields are filled in before submitting

## Future Enhancement Ideas

- Audio pronunciation support
- Spaced repetition algorithm
- Categories/tags for words
- Import/export word lists
- Multiple choice mode
- Difficulty levels

Enjoy learning Bahasa Indonesian! 🇮🇩🇬🇧
