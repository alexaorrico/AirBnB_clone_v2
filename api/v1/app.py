#!/usr/bin/python3
"""
Create an app instance
"""
import os
from flask import Flask
from flask import jsonify
from flask_cors import CORS

from . import models
from .views import app_views

app = Flask(__name__)
CORS(app, resources=r"/*", origins=["0.0.0.0"])

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(e=None):
    """
    Registers a function to be called after each request and app processs
    """
    models.storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    Handling not found (404)
    Args:
        e: Exception
    Returns:
        JSON
    """
    status_code = str(e).split()[0]
    message = e.description if "Not found" in e.description else "Not found"
    return jsonify({"error": message}), status_code


@app.errorhandler(400)
def bad_request(e):
    """
    Handling bad request (400)
    Args:
        e: Exception
    Returns:
        JSON
    """
    status_code = str(e).split()[0]
    message = e.description
    return jsonify({"error": message}), status_code


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
