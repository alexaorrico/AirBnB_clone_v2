#!/usr/bin/python3
"""
Main Flask application for the AirBnB clone API.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(exception):
    """
    Closes the storage on teardown.

    Args:
        exception: Unused argument.

    Returns:
        None
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Custom error handler for 404 errors.

    Returns a JSON-formatted 404 status code response.

    Args:
        error: The error message.

    Returns:
        JSON response with a 404 status code and "error": "Not found".
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
