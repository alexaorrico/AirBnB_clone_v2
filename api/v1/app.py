#!/usr/bin/python3
"""Module for start the API"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(self):
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST') or "0.0.0.0"
    HBNB_API_PORT = getenv('HBNB_API_PORT') or 5000
    app.run(
        host=HBNB_API_HOST,
        port=int(HBNB_API_PORT),
        threaded=True,
        debug=True
        )
