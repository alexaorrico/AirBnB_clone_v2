#!/usr/bin/python3
""" The implemtation of tha application"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(exc=None):
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=HOST, port=PORT, threaded=True)
