#!/usr/bin/python3
"""This file return the status of the API"""
import os
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint, make_response
from models import storage
"""from flask_cors import CORS"""

app = Flask(__name__)
app.register_blueprint(app_views)
"""cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})"""


@app.teardown_appcontext
def teardown(exc):
    """Remove the session after each request"""
    storage.close()


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
