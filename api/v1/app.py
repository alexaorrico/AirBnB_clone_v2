#!/usr/bin/python3
"""
Module for handling Flask application and API routes.
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False


CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Teardown App Context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 status code"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    """Teardown App Context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 status code"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
