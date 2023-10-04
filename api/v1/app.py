#!/usr/bin/python3
"""The `app` module implements a Flask application for HBNB"""


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Defines a teardown function that
    closes storage connections
    """
    storage.close()


@app.errorhandler(404)
def _handler_api(exception):
    """Hanldes 404 page not found error"""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")
    if not HBNB_API_HOST:
        host = "0.0.0.0"
    else:
        host = HBNB_API_HOST
    if not HBNB_API_PORT:
        port = 5000
    else:
        port = HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
