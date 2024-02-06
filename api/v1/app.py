#!/usr/bin/python3
"""
This module contains our first version of the api
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closing(exception):
    """tear down method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Not found method"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hostname = os.getenv('HBNB_API_HOST')
    portnum = os.getenv('HBNB_API_PORT')
    if not hostname:
        hostname = '0.0.0.0'
    if not portnum:
        portnum = 5000
    app.run(host=hostname, port=portnum, threaded=True)
