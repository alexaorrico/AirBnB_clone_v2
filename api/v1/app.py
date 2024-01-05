#!/usr/bin/python3
"""
creates a Flask web application
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """ runs after every request """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ handles the 404 error """
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """ handles the 400 error """
    message = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        message = error.description
    return jsonify(error=message), 400


if __name__ == '__main__':
    app.run(
        port=app_port,
        host=app_host,
        threaded=True
    )
