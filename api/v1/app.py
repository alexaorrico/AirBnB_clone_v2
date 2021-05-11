#!/usr/bin/python3
"""Flask Setup"""

from models import storage
from api.v1.views import app_views
import flask
from flask import request, jsonify
from os import environ
from flask_cors import CORS

app = flask.Flask(__name__)

# CORS instance
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """404 error"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def page_not_found2(err):
    """400 error"""
    return jsonify({"error": err.description}), 400


if __name__ == "__main__":
    env_host = environ.get('HBNB_API_HOST', default='0.0.0.0')
    env_port = environ.get('HBNB_API_PORT', default=5000)
    app.run(host=env_host, port=int(env_port), threaded=True)
