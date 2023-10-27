#!/usr/bin/python3
"""
Main application module for the AirBnB API.

This module creates a Flask application, registers blueprints,
and handles app context teardown.
"""
from flask import Flask, Blueprint, jsonify, make_response
from os import environ
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


# Create a Flask app
app = Flask(__name__)

# Register the blueprint app_views with a URL prefix
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


# Define a method to handle app context teardown
@app.teardown_appcontext
def teardown_appcontext(code):
    """
    Teardown the Flask app context and close the database connection.

    This function is automatically called when the app context is popped.

    :param exception: An exception object (not used in this function).
    """
    storage.close()


# Define a handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 errors and return a JSON-formatted 404 response.

    :param error: The 404 error object.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Get the host and port from environment variables or use defaults
    app.run(host=environ.get('HBNB_API_HOST', '0.0.0.0'),
            port=int(environ.get('HBNB_API_PORT', 5000)))
