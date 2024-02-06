#!/usr/bin/python3
""" The implemtation of tha application"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': ['0.0.0.0']}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(exc=None):
    """ Tear down context to tear app down"""
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    """ Error handler for 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
