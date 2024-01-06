#!/usr/bin/python3
"""Wrapper of AirBnB web app built using Flask"""

from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exc):
    """Closes the current storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """Return page not found message in JSON format"""
    return jsonify({"error": "Not found"})


host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = int(getenv("HBNB_API_PORT", default="5000"))

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True, debug=True)
