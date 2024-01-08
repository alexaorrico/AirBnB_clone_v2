#!/usr/bin/python3
"""Wrapper of AirBnB web app built using Flask"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response
from flask_cors import CORS
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_session(exc):
    """Closes the current storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """Return page not found message in JSON format"""
    return make_response(jsonify({"error": "Not found"}), 404)


host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = int(getenv("HBNB_API_PORT", default="5000"))

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
