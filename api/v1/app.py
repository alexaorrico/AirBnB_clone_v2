#!/usr/bin/python3
"""
This module sets up the Flask application, configures
CORS, registers blueprints,
handles teardown context,  and customizes error handling.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage

"""Create a Flask application instance """
app = Flask(__name__)

""" set up CORS to allow request from origin """
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

"""Register blueprint with flask app """
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Close the storage engine at the end of the request.
    :param exception: Exception raised, if any

    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handle 404 errors by returning a JSON response.
    :param exception: Exception raised , typically a 404 error
    :return: JSON response with error message and 404 status code

    """
    data = {
            "error": "Not found"
            }
    response = jsonify(data)
    response.status_code = 404

    return response


if __name__ == "__main__":
    """ Run the flask app using host and port from environment variables """
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=int(getenv("HBNB_API_PORT", 5000)),
            threaded=True)
