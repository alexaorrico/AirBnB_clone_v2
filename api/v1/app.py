#!/usr/bin/python3
""" Flask Application """
from flask import Flask, jsonify, make_response
from os import getenv
from models import storage
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean(exe):
    """Closes the Storage."""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """404 Error"""
    error = {
        "error": "Not found"
    }
    return make_response(jsonify(error), 404)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"), threaded=True)
