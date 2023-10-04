#!/usr/bin/python3
"""
Module for the main Flask application.
"""

from flask_cors import CORS
from flask import Flask, jsonify
import json
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Tears down the app context, closes the storage.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Custom 404 error handler that returns a JSON-formatted 404 status
    code response.
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return json.dumps(response.get_json(), indent=2) + '\n', 404


if __name__ == "__main__":
    host = "0.0.0.0" if not getenv(
        "HBNB_API_HOST") else getenv("HBNB_API_HOST")
    port = 5000 if not getenv(
        "HBNB_API_PORT") else int(getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)
