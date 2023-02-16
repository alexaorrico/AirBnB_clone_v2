#!/usr/bin/python3

"""Bootstap for api"""

from api.v1.views import app_views
from models import storage
from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """if route does not exist"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST", "0.0.0.0"), getenv(
        "HBNB_API_PORT", 5000), threaded=True)
