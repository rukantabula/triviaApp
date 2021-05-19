import os
from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  @cross_origin()
  def get_categories():
    categories = Category.query.all()
    if len(categories) == 0:
      abort(404)

    formated_categories = [category.format() for category in categories]

    category_list = []
    for category in formated_categories:
      category_list.append(category['type'])

    return jsonify({
      'success': True,
      'categories': category_list
    })

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
  @app.route('/questions', methods=['GET'])
  @cross_origin()
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    if len(questions) == 0:
      abort(404)

    formatted_questions = [question.format() for question in questions]
    category_results = []
    categories = Category.query.all()
    if len(categories) == 0:
      abort(404)

    formated_categories = [category.format() for category in categories]
    if len(formatted_questions[start:end]) == 0:
      abort(404)

    for category in formated_categories:
      category_results.append(category['type'])

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'categories': category_results
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  @cross_origin()
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      db.session.delete(question)
      Question.query.filter(Question.id == question_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()
    return jsonify({
      'success': True,
      'status': 'question deleted'
    })

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
  def create_question():
    try:
      body = request.get_json()
      question = Question(
          question = body['question'],
          answer = body['answer'],
          category = body['category'],
          difficulty = body['difficulty']
        )


      db.session.add(question)
      db.session.commit()
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()
    return jsonify({
      'success': True,
      'status': 'Question added'
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm'].strip().lower()
    questions = Question.query.all()
  
    if len(questions) == 0:
      abort(404)

    formatted_questions = [question.format() for question in questions]
    search_results = []

    if not len(search_term) == 0:
      for term in formatted_questions:
        if search_term in term['question'].lower():
          search_results.append(term)
    else:
      abort(422)

    return jsonify({
      'success': True,
      'questions': search_results
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  @cross_origin()
  def get_questions_by_category(category_id):
    questions = Question.query.filter(Question.category == category_id + 1).all()
    if len(questions) == 0:
      abort(404)

    formatted_questions = [question.format() for question in questions]
    return jsonify({
      'success': True,
      'questions': formatted_questions
    })

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
  def get_questions_to_play():
    body = request.get_json()
    previous_questions = body['previous_questions']
    quiz_category = body['quiz_category']
    questions = Question.query.filter(Question.category == int(quiz_category['id']) + 1).all()
    if len(questions) == 0:
      abort(404)

    formatted_questions = [question.format() for question in questions]
    selected_question = ''
    random_question = random.choice(formatted_questions)

    if random_question not in previous_questions:
      selected_question = random_question

    return jsonify({
      'success': True,
      'question': selected_question
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found_error(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
      }), 400

  @app.errorhandler(404)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
      }), 404

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Server Error"
      }), 500

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "The request can't be processed"
      }), 422

  return app