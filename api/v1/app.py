#!/usr/bin/python3
"""Flask app implementation with blueprint"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
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
    """Closes database storage"""
    storage.close()


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    if isinstance(e, HTTPException):
        if type(e).__name__ == "NotFound":
            e.description = "Not found"
            dsp = {"error": e.description}
            cod = e.code
        else:
            dsp = {"error": e}
            cod = 500
        return make_response(jsonify(dsp), cod)


def setup_error_handler():
    """
    updates HTTPException class with error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, handle_exception)


if __name__ == "__main__":
    """Flask runner"""
    setup_error_handler()
    app.run(host=host, port=port, threaded=True)
