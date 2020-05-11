import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from flask import jsonify


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.valid_question = {
            'question': 'question',
            'answer': 'answer',
            'category': 2,
            'difficulty': 3
        }

        self.invalid_question = {
            'invalidquestion': 'xxx'
        }

        self.valid_question_to_play = {
            'previous_questions' : [29,22],
            'quiz_category': {
                'type': 'Art',
                'id': '1'}
        }

        self.no_question_to_play = {
            'previous_questions' : [],
            'quiz_category': {
                'type': 'Science',
                'id': '0'}
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(res.status_code, 200)
        
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(res.status_code, 200)

    def test_get_questions_with_valid_page(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(res.status_code, 200)

    def test_404_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['status'],'question deleted')
        self.assertEqual(question, None)
        self.assertEqual(res.status_code, 200)

    def test_delete_question_with_invalide_id(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5000).one_or_none()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'],'Server Error')
        self.assertEqual(res.status_code, 500)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.valid_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status'],'Question added')
        self.assertEqual(res.status_code, 200)

    def test_add_question_with_invalid_body(self):
        res = self.client().post('/questions', json=self.invalid_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'],'Server Error')
        self.assertEqual(res.status_code, 500)

    def test_search_question(self):
        res = self.client().post('/questions/search', json={'searchTerm':'country'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['questions'][0]['question'])
        self.assertTrue(data['questions'][0]['category'])
        self.assertTrue(data['questions'][0]['difficulty'])
        self.assertTrue(data['questions'][0]['id'])
        self.assertTrue(data['questions'][0]['answer'])
        self.assertEqual(res.status_code, 200)

    def test_search_question_with_empty_search_term(self):
        res = self.client().post('/questions/search', json={'searchTerm':''})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'],'The request can\'t be processed')
        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category_with_invalid_id(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(res.status_code, 404)

    def test_play_quizz(self):
        res = self.client().post('/quizzes', json=self.valid_question_to_play)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(res.status_code, 200)

    def test_play_quizz_with_no_question_for_category(self):
        res = self.client().post('/quizzes', json=self.no_question_to_play)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()