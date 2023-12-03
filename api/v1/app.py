#!/usr/bin/python3
"""Flask application serving our API"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def handle_close(err):
    """Closes the storage connection"""
    storage.close()


@app.errorhandler(404)
def handle_page_not_found(err):
    """Handles 404 errors by returning a JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"), threaded=True)
