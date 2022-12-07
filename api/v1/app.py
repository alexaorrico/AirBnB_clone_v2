#!/usr/bin/python3
""" Create api """

from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def closedb(exit):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    returns a 404 JSON error response
    jsonify() serializes data to json
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST") or '0.0.0.0'
    port = os.getenv("HBNB_API_PORT") or '5000'
    app.run(host=host, port=port, threaded=True)