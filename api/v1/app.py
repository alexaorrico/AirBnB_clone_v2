#!/usr/bin/python3
"""App on flask"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.teardown_appcontext
def teardown_appcontext(Exception):
    """close session on storage"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)
