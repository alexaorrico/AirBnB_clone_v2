#!/usr/bin/python3
"""Contains app, instance of Flask"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """tear down storages"""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """Handle not found pages"""
    data = {
                "error": "Not found"
           }
    response = jsonify(data)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
