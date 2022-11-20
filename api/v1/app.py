#!/usr/bin/python3
"""This module contains the base start up for flask in this proect."""

from os import getenv
from flask import Flask, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.teardown_appcontext
def tear_down(exception):
    storage.close()

@app.errorhandler(404)
def handle_404(error):
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
