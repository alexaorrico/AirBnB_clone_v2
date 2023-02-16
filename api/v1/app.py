#!/usr/bin/python3
"""
This module contains the Flask application instance and the API routes.
The application instance is created and the API routes are registered here.

Usage:
    You can run this module to start the Flask web server.

    To run the server with default configuration, run:
        python -m api.v1.app

    You can also set the environment variables :
        HBNB_API_HOST
        HBNB_API_PORT
    to configure the server host and port respectively.
"""
from flask import Flask
import models
from api.v1.views import app_views
import os


# flask application instance
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_flask(exception):
    """
    request context end event listener.
    """
    # print(exception)
    models.storage.close()

#400 error handler
@app.errorhandler(400)
def error_400(error):
    """
    Handles the 400 HTTP error code.
    """
    message = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        message = error.description
    return jsonify(error=message), 400

# 404 error handler defination
@app.errorhandler(404)
def page_not_found(error):
    """
    return a JSON-formatted 404 status code response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    runs flask web server
    """
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
