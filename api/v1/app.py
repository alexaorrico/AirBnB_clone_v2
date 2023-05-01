#!/usr/bin/python3
""" start flask """

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear(exception=None):
    """ tear down"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ page not found """
    return jsonify(e="Not found"), 404


if __name__ == '__main__':
    h = getenv('HBNB_API_HOST')
    p = getenv('HBNB_API_PORT')
    app.run(host=h, port=h, threaded=True)
