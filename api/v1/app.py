#!/usr/bin/python3
"""Flask app implementation with blueprint"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv
from werkzeug.exceptions import HTTPException


host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", 5000)

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": host}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage"""
    storage.close()


@app.errorhandler(Exception)
def error_handler(error):
    """Handles 404 error"""
    if isinstance(error, HTTPException):
        if type(error).__name__ == "NotFound":
            error.description = "Not found"
        msg = error.description
        code = error.code
    else:
        msg = error
        code = 500
    return make_response(jsonify({"error": msg}), code)


def setup_error_handler():
    """
    updates HTTPException class with error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, error_handler)


if __name__ == "__main__":
    """Flask runner"""
    setup_error_handler()
    app.run(host=host, port=port, threaded=True)
