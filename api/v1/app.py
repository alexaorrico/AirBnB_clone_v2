#!/usr/bin/python3
"""Module app.py: starts the flask app"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error='Not found'), 404


@app.teardown_appcontext
def tear_down(Exception):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)
