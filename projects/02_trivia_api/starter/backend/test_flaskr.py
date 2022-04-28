import os
import unittest
import json

from sqlalchemy import false
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from test_config import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = user_id
        self.user_password = user_password
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.user_name, self.user_password, 'localhost:5432', self.database_name)
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertTrue(len(result.get('categories')))

    def test_get_questions(self):
        res = self.client().get('/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertTrue(result.get('totalQuestions'))
        self.assertTrue(len(result.get('questions')))

    def test_delete_question(self):
        # create a question and then test deleting it
        question = Question(question='Test Question', answer='Test Answer1', difficulty=int(3), category='3')
        question.insert()
        question_id = question.id
        all_questions_before_del = Question.query.all()
        
        res = self.client().delete('questions/{}'.format(question_id))
        result = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('deleted'), question_id)
        all_questions_after_del = Question.query.all()
        self.assertTrue(len(all_questions_before_del) - len(all_questions_after_del) == 1)
        # Validate if deleted id exist in db
        question_deleted = Question.query.filter(Question.id == question_id).one_or_none()
        self.assertIsNone(question_deleted)

    def test_create_question(self):
        questions_before_create = Question.query.all()
        #question to create
        question_to_create = {
            'question': 'Test Create Question',
            'answer': 'Test create answer',
            'difficulty': 1,
            'category': '1'
        }

        res = self.client().post('/questions', json=question_to_create)
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        questions_after_create = Question.query.all()
        question_created = Question.query.filter_by(id=result.get('created')).one_or_none()
        self.assertTrue(len(questions_after_create) - len(questions_before_create) == 1)
        self.assertIsNotNone(question_created)

    def test_search_question(self):
        # create a question and then test searching it
        question = Question(question='Test Question to search', answer='Test Answer1', difficulty=int(3), category='3')
        question.insert()
        search_item = {
            'searchTerm': 'search'
        }
        res = self.client().post('/questions', json=search_item)
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertNotEqual(result.get('total_questions'), 0)
    
    def test_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertNotEqual(result.get('totalQuestions'), 0)

    def test_quizzes(self):
        json_to_send = {
            'previous_questions': [20, 21],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        }

        res = self.client().post('/quizzes', json=json_to_send)
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result.get('success'))
        self.assertTrue(result.get('question'))
        self.assertNotEqual(result.get('question')['id'], 20)
        self.assertNotEqual(result.get('question')['id'], 21)

    # Testing errors
    def test_pagination_error(self):
        res = self.client().get('/questions?page=1000')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(result.get('success'))
        self.assertTrue(result.get('message'), 'resource not found')

    def test_deletion_non_existing_question(self):
        res = self.client().delete('/question/40000')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(result.get('success'))
        self.assertEqual(result.get('message'), 'resource not found')

    def test_get_questions_for_category_that_does_not_exist(self):
        res = self.client().get('/categories/notACategory/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(result.get('success'))
        self.assertTrue(result.get('message'), 'resource not found')

    def test_quiz_error(self):
        json_to_send = {'previous_questions': []}
        res = self.client().post('/quizzes', json=json_to_send)
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(result.get('success'))
        self.assertEqual(result.get('message'), 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()