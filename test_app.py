import unittest
import json
from app import app, get_db, init_db, DATABASE
import os

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        # Ensure a clean database for each test
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
        init_db() # Initialize with sample data

    def tearDown(self):
        # Clean up the database after each test
        if os.path.exists(DATABASE):
            os.remove(DATABASE)

    def test_add_phrase(self):
        # Test adding a phrase successfully
        response = self.app.post(
            '/api/add_phrase',
            data=json.dumps({'indonesian_phrase': 'Selamat siang', 'english_phrase': 'Good afternoon'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Phrase added successfully')

        # Verify the phrase is in the database
        conn = get_db()
        cursor = conn.execute('SELECT indonesian_phrase, english_phrase FROM phrases WHERE indonesian_phrase = ?', ('Selamat siang',))
        phrase = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(phrase)
        self.assertEqual(phrase['english_phrase'], 'Good afternoon')

    def test_add_phrase_missing_fields(self):
        # Test adding a phrase with missing fields
        response = self.app.post(
            '/api/add_phrase',
            data=json.dumps({'indonesian_phrase': 'Selamat malam'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Both fields are required')

    def test_get_phrases(self):
        # Test retrieving phrases
        response = self.app.get('/api/phrases')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0) # Should contain sample phrases
        self.assertIn({'id': 1, 'indonesian_phrase': 'Apa kabar?', 'english_phrase': 'How are you?'}, data)

if __name__ == '__main__':
    unittest.main()