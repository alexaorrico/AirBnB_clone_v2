#!/usr/bin/python3
"""Mudule which contains the FLASK_APP and represents the entry point"""
from flask_cors import CORS
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    """Method which tears down storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Method which returns 404 error in a JSON format"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
