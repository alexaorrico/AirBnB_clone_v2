#!/usr/bin/python3
""" Module for first API """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or 5000


@app.teardown_appcontext
def close(self):
    """ Method closes current session """
    storage.close()


@app.errorhandler(404)
def status_404(e):
    """ Method handles 404 response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
