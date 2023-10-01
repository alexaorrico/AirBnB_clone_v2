#!/usr/bin/python3
"""Create a Flask API"""

from flask import Flask, jsonify, make_response
import os
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

"""Instantiate a flask app by calling the Flask class"""
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


def close_storage(exception=None):
    """method to handle app context storage"""
    storage.close()


"""Register the teardown function"""
app.teardown_appcontext(close_storage)


@app.errorhandler(404)
def not_found(error):
    """Returns the page Not Found in JSON format"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, debug=True, threaded=True)
