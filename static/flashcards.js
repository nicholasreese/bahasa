let words = [];
let currentIndex = 0;
let currentAttempt = 1;
let quizMode = ''; // 'indonesian' or 'english'
let correctAnswers = 0;
let incorrectAnswers = 0;
let shuffledWords = [];

// Load words when page loads
// loadWords();

async function loadWords() {
    try {
        const response = await fetch('/api/words');
        words = await response.json();
        
        if (words.length === 0) {
            alert('No words available! Please add some words first.');
            window.location.href = '/add_word';
        }
    } catch (error) {
        console.error('Error loading words:', error);
        alert('Error loading words. Please try again.');
    }
}

async function startQuiz(mode) {
    if (words.length === 0) {
        await loadWords(); // Ensure words are loaded before starting quiz
        if (words.length === 0) {
            alert('No words available! Please add some words first.');
            window.location.href = '/add_word';
            return;
        }
    }
    
    quizMode = mode;
    currentIndex = 0;
    currentAttempt = 1;
    correctAnswers = 0;
    incorrectAnswers = 0;
    
    // Shuffle words for the quiz
    shuffledWords = [...words].sort(() => Math.random() - 0.5).slice(0, 20);
    
    // Hide selection, show quiz
    document.getElementById('languageSelection').classList.add('hidden');
    document.getElementById('quizContainer').classList.remove('hidden');
    
    // Update total cards
    document.getElementById('totalCards').textContent = shuffledWords.length;
    
    // Show first card
    showCard();
}

function showCard() {
    if (currentIndex >= shuffledWords.length) {
        showResults();
        return;
    }
    
    const word = shuffledWords[currentIndex];
    const questionWord = quizMode === 'indonesian' ? word.indonesian : word.english;
    
    document.getElementById('questionWord').textContent = questionWord;
    document.getElementById('currentCard').textContent = currentIndex + 1;
    document.getElementById('attemptNumber').textContent = currentAttempt;
    
    // Update progress bar
    const progress = ((currentIndex) / shuffledWords.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    
    // Reset input and buttons
    document.getElementById('answerInput').value = '';
    document.getElementById('answerInput').disabled = false;
    document.getElementById('answerInput').focus();
    document.getElementById('submitBtn').style.display = 'inline-block';
    document.getElementById('feedback').classList.add('hidden');
    document.getElementById('resultButtons').classList.add('hidden');
    
    currentAttempt = 1;
}

function checkAnswer() {
    const userAnswer = document.getElementById('answerInput').value.trim().toLowerCase();
    const currentWord = shuffledWords[currentIndex];
    const correctAnswer = quizMode === 'indonesian' ? 
        currentWord.english.toLowerCase() : 
        currentWord.indonesian.toLowerCase();
    
    if (!userAnswer) {
        alert('Please enter an answer!');
        return;
    }
    
    const feedback = document.getElementById('feedback');
    feedback.classList.remove('hidden', 'correct', 'incorrect', 'show-answer');
    
    // Check if answer is correct
    if (userAnswer === correctAnswer) {
        // Correct answer
        // Correct answer
        feedback.classList.add('correct');
        feedback.textContent = `Correct! The answer is "${quizMode === 'indonesian' ? currentWord.english : currentWord.indonesian}".`;
        correctAnswers++;
        document.getElementById('answerInput').disabled = true;
        document.getElementById('submitBtn').style.display = 'none';
        document.getElementById('resultButtons').classList.remove('hidden');
    } else {
        // Incorrect answer
        currentAttempt++;
        if (currentAttempt <= 2) {
            feedback.classList.add('incorrect');
            feedback.textContent = `Incorrect. Try again! (Attempt ${currentAttempt} of 2)`;
            document.getElementById('attemptNumber').textContent = currentAttempt;
        } else {
            incorrectAnswers++;
            feedback.classList.add('show-answer');
            feedback.textContent = `Incorrect. The correct answer was "${correctAnswer}".`;
            document.getElementById('answerInput').disabled = true;
            document.getElementById('submitBtn').style.display = 'none';
            document.getElementById('resultButtons').classList.remove('hidden');
        }
    }
    updateProgress();
}

function nextCard() {
    currentIndex++;
    showCard();
}

function showResults() {
    document.getElementById('quizContainer').classList.add('hidden');
    document.getElementById('resultsContainer').classList.remove('hidden');
    
    const total = correctAnswers + incorrectAnswers;
    const accuracy = total > 0 ? Math.round((correctAnswers / total) * 100) : 0;
    
    document.getElementById('correctCount').textContent = correctAnswers;
    document.getElementById('incorrectCount').textContent = incorrectAnswers;
    document.getElementById('accuracyPercent').textContent = accuracy + '%';
}

function restartQuiz() {
    document.getElementById('quizContainer').classList.add('hidden');
    document.getElementById('resultsContainer').classList.add('hidden');
    document.getElementById('languageSelection').classList.remove('hidden');
}

// Allow Enter key to submit answer
document.addEventListener('DOMContentLoaded', function() {
    const answerInput = document.getElementById('answerInput');
    if (answerInput) {
        answerInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !this.disabled) {
                checkAnswer();
            }
        });
    }
});

// Event Listeners for practice mode selection
document.addEventListener('DOMContentLoaded', async () => {
    await loadWords(); // Ensure words are loaded before attaching event listeners

    document.getElementById('practiceIndonesianBtn').addEventListener('click', () => {
        startQuiz('indonesian');
    });

    document.getElementById('practiceEnglishBtn').addEventListener('click', () => {
        startQuiz('english');
    });
});
