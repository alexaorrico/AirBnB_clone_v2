#!/usr/bin/python3
"""Proceeds to import Flask and run host plus port"""


from api.v1.views import app_views
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from models import storage
from os import environ
from werkzeug.exceptions import NotFound
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Makes a call to storage.close() to close session"""
    storage.close()


@app.errorhandler(NotFound)
def handle_404(error):
    """Creates custom 404 page incase of 404 error code"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == '__main__':
    hst = environ.get("HBNB_API_HOST") if environ.get(
            "HBNB_API_HOST") else "0.0.0.0"
    prt = environ.get("HBNB_API_PORT") if environ.get(
            "HBNB_API_PORT") else 5000
    app.run(host=hst, port=prt, threaded=True)
