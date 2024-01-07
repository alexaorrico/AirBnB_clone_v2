#!/usr/bin/python3
"""This script represents the primary Application"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv


app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.errorhandler(NotFound)
def not_found(error):
    """This function loads a custom page 404 errors NotFound"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def tear_down_context(exception):
    """This function removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST",)
    port = getenv("HBNB_API_PORT",) 

      if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
