#!/usr/bin/python3
""" Module for first API """

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_down(self):
    """ Method closes current session """
    storage.close()


@app.errorhandler(404)
def status_404(e):
    """ Method handles 404 response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if environ.get("HBNB_API_HOST"):
        host = environ.get("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if environ.get("HBNB_API_PORT"):
        port = environ.get("HBNB_API_PORT")
    else:
        port = "5000"
    app.run(host=host, port=port, threaded=True)