#!/usr/bin/python3
"""
API for HBNB
"""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={'/*': {'origins': ['0.0.0.0']}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    ''' Close SQLAlchemy session '''

    storage.close()


@app.errorhandler(404)
def handle_not_found(err=None):
    """
    Handler for 404 errors that returns
    a JSON-formatted 404 status code response
    """
    return (jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST', '0.0.0.0'),
            int(getenv('HBNB_API_PORT', '5000')), threaded=True)
