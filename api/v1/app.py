#!/usr/bin/python3

"""
api
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv
from flask_cors import CORS

"""module: Index
"""
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """Method to handle teardown of the application context."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """page_not_found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
