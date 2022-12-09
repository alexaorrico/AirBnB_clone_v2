#!/usr/bin/python3
"""app"""

from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default='5000')
    app.run(host=hosts, port=ports, threaded=True)
