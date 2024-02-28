#!/usr/bin/python3
"""This is the Flask module for our API."""


from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
import json


"""start flask"""
app = Flask(__name__)

"""regiser blueprint"""
app.register_blueprint(app_views)


"""  HTTP access control (CORS) """
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def close_app(exception):
    """this closes the app

    Args:
        exception (_type_): _description_
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """this handles page not found error"""
    return json.dumps({"error": "Not found"}, indent=2), 404


if __name__ == "__main__":
    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
