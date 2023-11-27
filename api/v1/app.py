#!/usr/bin/python3
"""
This script sets up a Flask
application with API endpoints.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from werkzeug.exceptions import HTTPException
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(e=None):
    """
    Closes the storage after each request.

    Args: e (Exception, optional):

    An exception that was raised during the request.
    """
    storage.close()


@app.errorhandler(HTTPException)
def not_found(e):
    """
    Handles HTTP exceptions by returning a
    JSON response with an error message.

    Args:
        e (HTTPException): The exception that was raised.

    Returns:
        Response: A Flask Response object with a
        JSON body containing the error message.
    """
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "error": "Not found"
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    """
    Runs the Flask application.
    """
    if getenv('HBNB_API_HOST') is not None:
        the_host = getenv('HBNB_API_HOST')
    else:
        the_host = '0.0.0.0'
    if getenv('HBNB_API_PORT') is not None:
        the_port = getenv('HBNB_API_PORT')
    else:
        the_port = 5000
    app.run(host=the_host, port=the_port, threaded=True)
