#!/usr/bin/python3
"""module for app file of hbnb clone"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from flask import Blueprint
from os import environ
from flask_cors import CORS


# set up app_views blueprint and flask instance
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """close storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return make_response({"error": "Not found"}), 404


if __name__ == "__main__":
    """Main """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
