#!/usr/bin/python3
"""Starts a Flask API application."""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_funtion(n):
    """close funtion."""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host=os.environ.get('HBNB_API_HOST'),
            port=os.environ.get('HBNB_API_PORT'), threaded=True, debug=True)
