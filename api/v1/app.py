#!/usr/bin/python3
"""
This is to create variable app instance of Flask
"""
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
import os

app = Flask(__name__)
"""
this is for falk instances
"""
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_handler(exception):
    """
    This is handle error 404
    """
    storage.close()


@app.errorhanlder(404)
def not_found(error):
    """
    This is coustomized error handler
    """
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """
    This handles the 400 error
    """
    response = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        response = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=app_host, port=app_port, threaded=True)
