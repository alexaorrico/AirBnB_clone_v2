#!/usr/bin/python3
"""
Main application module for the AirBnB API.

This module creates a Flask application, registers blueprints,
and handles app context teardown.
"""

from flask import Flask
from os import environ
from api.v1.views import app_views
from models import storage


# Create a Flask app
app = Flask(__name__)

# Register the blueprint app_views with a URL prefix
app.register_blueprint(app_views, url_prefix='/api/v1')

# Define a method to handle app context teardown
@app.teardown_appcontext
def teardown(exception):
    """
    Teardown the Flask app context and close the database connection.

    This function is automatically called when the app context is popped.

    :param exception: An exception object (not used in this function).
    """
    storage.close()

if __name__ == "__main__":
    # Get the host and port from environment variables or use defaults
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)
