#!/usr/bin/python3
"""This module runs a flask server"""
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={'*': {'origins': '0.0.0.0'}})

app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """tears down the db after each request"""
    storage.close()


@app.errorhandler(404)
def error_404_handler(exception):
    """error handler for 404 responses"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST')
    PORT = os.getenv('HBNB_API_PORT')
    app.run(host=HOST if HOST is not None else '0.0.0.0',
            port=int(PORT) if PORT is not None else 5000,
            threaded=True, debug=True)
