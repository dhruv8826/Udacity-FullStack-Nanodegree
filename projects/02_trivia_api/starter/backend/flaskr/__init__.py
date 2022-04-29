import os
from queue import Empty
from flask import Flask, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	
	'''
	@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
	'''
	CORS(app, resources={'/': {'origins': '*'}})


	def category_list():
		categories = Category.query.all()
		category_json = {}
		for category  in categories:
			category_json[category.id] = category.type
		return category_json

	def paginate(request, selection):
		page = request.args.get('page', 1, type=int)
		start_id = (page -1) * QUESTIONS_PER_PAGE
		end_id = start_id + QUESTIONS_PER_PAGE

		items = [item.format() for item in selection]
		current_item = items[start_id:end_id]

		return current_item


	'''
	@TODO: Use the after_request decorator to set Access-Control-Allow
	'''
	@app.after_request()
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
		return response

	'''
	@TODO: 
	Create an endpoint to handle GET requests 
	for all available categories.
	'''
	@app.route('/categories')
	def get_categories():
		category_json = category_list()

		if (len(category_json) != 0):
				
			return jsonify({
				'success': True,
				'categories': category_json
			})

		else:
			abort(422)

	'''
	@TODO: 
	Create an endpoint to handle GET requests for questions, 
	including pagination (every 10 questions). 
	This endpoint should return a list of questions, 
	number of total questions, current category, categories. 

	TEST: At this point, when you start the application
	you should see questions and categories generated,
	ten questions per page and pagination at the bottom of the screen for three pages.
	Clicking on the page numbers should update the questions. 
	'''
	@app.route('/questions')
	def get_questions():
		all_questions = Question.query.order_by(Question.id).all()
		current_questions = paginate(request, all_questions)

		if (len(current_questions) == 0):
			abort(404)

		category_json = category_list()

		if (len(current_questions) != 0):
			return jsonify({
				'success': True,
				'questions': current_questions,
				'totalQuestions': len(all_questions),
				'categories': category_json,
				'currentCategory': None
			})
		else:
			abort(422)

	'''
	@TODO: 
	Create an endpoint to DELETE question using a question ID. 

	TEST: When you click the trash icon next to a question, the question will be removed.
	This removal will persist in the database and when you refresh the page. 
	'''
	@app.route('/questions/<int:question_id>', methods=['DELETE'])
	def delete_question(question_id):
		try:
			question_to_delete = Question.query.get(question_id)
			question_to_delete.delete()
			return jsonify({
				'success': True,
				'deleted': question_id
			})
		except:
			abort(422)

	'''
	@TODO: 
	Create an endpoint to POST a new question, 
	which will require the question and answer text, 
	category, and difficulty score.

	TEST: When you submit a question on the "Add" tab, 
	the form will clear and the question will appear at the end of the last page
	of the questions list in the "List" tab.  
	'''
	@app.route('/questions', methods=['POST'])
	def create_questions_or_search():
		read_input_json = request.get_json()

		if (read_input_json.get('searchTerm')):

			search_text = request.get_json().get('searchTerm')

			questions = Question.query.filter(Question.question.ilike(f'%{search_text}%')).all()

			if(len(questions) != 0):
				return jsonify({
					'success': True,
					'questions': [question.format() for question in questions],
					'total_questions': len(questions),
					'current_category': None
				})
			else:
				abort(422)

		else:
			question_details = read_input_json

			if not ('question' in question_details and 'answer' in question_details and 'category' in question_details and 'difficulty' in question_details):
				# flash('Something is missing in the request, please add all fields of the form')
				abort(422)

			try:
				question = Question(question=question_details.get('question'), answer=question_details.get('answer'), category=question_details.get('category'), difficulty=question_details.get('difficulty'))
				question.insert()

				return jsonify({
					'success': True,
					'created': question.id
				})
			except:
				abort(422)

	'''
	@TODO: 
	Create a POST endpoint to get questions based on a search term. 
	It should return any questions for whom the search term 
	is a substring of the question. 

	TEST: Search by any phrase. The questions list will update to include 
	only question that include that string within their question. 
	Try using the word "title" to start. 
	'''
	# Merged this with above method as test was failing on keeping them seperate

	'''
	@TODO: 
	Create a GET endpoint to get questions based on category. 

	TEST: In the "List" tab / main screen, clicking on one of the 
	categories in the left column will cause only questions of that 
	category to be shown. 
	'''
	@app.route('/categories/<int:category_id>/questions')
	def questions_based_on_category(category_id):
		category = Category.query.get(category_id)
		if (category == None):
			abort(404)
		questions = Question.query.filter_by(category=str(category_id)).all()

		if(len(questions) != 0):
			return jsonify({
				'success': True,
				'questions': [question.format() for question in questions],
				'totalQuestions': len(questions),
				'currentCategory': category.type
			})
		else:
			abort(422)


	'''
	@TODO: 
	Create a POST endpoint to get questions to play the quiz. 
	This endpoint should take category and previous question parameters 
	and return a random questions within the given category, 
	if provided, and that is not one of the previous questions. 

	TEST: In the "Play" tab, after a user selects "All" or a category,
	one question at a time is displayed, the user is allowed to answer
	and shown whether they were correct or not. 
	'''
	@app.route('/quizzes', methods=['POST'])
	def quize():
		input_info = request.get_json()
		category = input_info.get('quiz_category')
		previous_questions = input_info.get('previous_questions')

		if ((category is None) or (previous_questions is None)):
			abort(422)
		
		if (category['id'] == 0):
			questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
		else:
			questions = Question.query.filter_by(category=str(category['id'])).filter(Question.id.notin_(previous_questions)).all()
		
		if not (len(questions) == 0):
			question_to_return = questions[random.randrange(0, len(questions))].format()
		else:
			question_to_return = None
		
		return jsonify({
			'success': True,
			'question': question_to_return
		})

	'''
	@TODO: 
	Create error handlers for all expected errors 
	including 404 and 422. 
	'''
	@app.errorhandler(404)
	def handle_not_found(error):
		return jsonify({
			'success': False,
			'error': 404,
			'message': 'resource not found'
		}), 404

	@app.errorhandler(422)
	def handle_unprocessable(error):
		return jsonify({
			'success': False,
			'error': 422,
			'message': 'unprocessable'
		}), 422
	
	return app

		