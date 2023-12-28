#!/usr/bin/python3
"""this module contains a Flask APP"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """APP teardown method"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Initialize APP"""
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", "5000")),
        threaded=True)
