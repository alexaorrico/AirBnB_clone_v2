#!/usr/bin/python3
"""This module is responsible for the execution and management of the app."""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_storage(self):
    """Close session."""
    storage.close()


@app.errorhandler(404)
def page_not_found(self):
    """Handle 404 errors.

    Returns:
        dict: Returns a JSON-formatted 404 status code response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    h = getenv("HBNB_API_HOST", "0.0.0.0")
    p = getenv("HBNB_API_PORT", 5000)
    app.run(debug=True, host=h, port=p, threaded=True)
