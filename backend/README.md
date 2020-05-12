# Full Stack Trivia API Backend

This project is a meant to create social bonding experience for udacity employees and students via a Trivia game experience.
Users would be to both add questions and specificy the difficulty level and question's category and play and enoy the game!

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Reference

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```


## Endpoints
### GET/categories

The endpoint handles requests for available categories. 

url: http://127.0.0.1:5000/categories

Request Response
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}

```

### GET/questions

The endpoint handles requests for questions, including pagination (every 10 questions). This endpoint returns a list of questions, number of total questions, current category, categories. 

url: http://127.0.0.1:5000/questions

Request Response
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
    ...
  ],
  "success": true,
  "total_questions": 21
}

```

### DELETE/questions/{question_id}

The endpoint handles requests to DELETE question using a question ID. 

url: http://127.0.0.1:5000/questions/5

Request Response
```
{
  "status": "Question deleted",
  "success": true
}

```

### POST/questions

The endpoint handles requests to POST a new question

url: http://127.0.0.1:5000/questions

Request Body: 
```
{
  "question": "question",
  "answer": "answer",
  "category": 2,
  "difficulty": 3
}

```

Request Response
```
{
  "status": "Question added",
  "success": true
}

```

### POST/questions/search

The endpoint handles requests to get questions based on a search term. It returns any questions for whom the search term is a substring of the question.

url: http://127.0.0.1:5000/questions/search

Request Body: 
```
{
  "searchTerm": "country"
}

```

Request Response
```
{
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true
}

```

### GET/categories/{category_id}/questions

The endpoint handles requests to get questions based on category. 

url: http://127.0.0.1:5000/categories/4/questions

Request Response
```
{
  "questions": [
    {
      "answer": "yes",
      "category": 5,
      "difficulty": 1,
      "id": 30,
      "question": "science"
    }
  ],
  "success": true
}
```

### POST/quizzes

The endpoint handles requests to get questions to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 

url: http://127.0.0.1:5000/quizzes

Request Body: 
```
{
 "previous_questions" : [],
 "quiz_category": {
 "type": "Geography",
 "id": "2"
  }
}

```

Request Response
```
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```