#!/usr/bin/python3
"""app"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_call(self):
    """call"""
    storage.close()


@app.errorhandler(404)
def error_found(e):
    """found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'

    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = '5000'

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
