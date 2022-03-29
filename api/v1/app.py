#!/usr/bin/python3
"""Registers Blueprint + Error 404 + Teardown"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
CORS(app, origins=["http://0.0.0.0/*"], allow_headers='*')

app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(appcontext):
    """shuts down the database"""
    storage.close()


if __name__ == '__main__':
    if environ.get('HBNB_API_HOST') is not None:
        host = environ.get('HBNB_API_HOST')
    else:
        host = "0.0.0.0"
    if environ.get('HBNB_API_PORT') is not None:
        port = environ.get('HBNB_API_PORT')
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)