#!/usr/bin/python3
"""Initializes the Flask application"""

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Called to close the storage after each request"""
    storage.close()


@app.errorhandler(404)
def handler_error(stat):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
