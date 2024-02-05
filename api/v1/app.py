#!/usr/bin/python3
"""
Flask web application API initialization and configuration.
This module sets up Flask, CORS, registers blueprints for API views,
and defines error handlers and teardown actions.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

# CORS setup allowing all origins for the entire app
CORS(app, resources={r"/*": {"origins": app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """
    Ensures the closing of the storage on app teardown.
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    Custom error handler for 404 errors.
    """
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """
    Custom error handler for 400 errors.
    """
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=app_host, port=app_port, threaded=True)
