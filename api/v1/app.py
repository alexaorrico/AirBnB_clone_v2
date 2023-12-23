#!/usr/bin/python3
"""Main module for Flask app"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Custom error handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", "5000")),
        threaded=True
    )
