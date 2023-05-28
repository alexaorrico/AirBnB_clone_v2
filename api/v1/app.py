#!/usr/bin/python3
"""Flask RESTful API.

This initializes the Flask app for our AirBnB
Clone.

"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(Exception):
    """Clear the storage and end the current session."""
    try:
        storage.close()
    except Exception:
        exit(1)


@app.errorhandler(404)
def not_found(error):
    """Handle the 404 Status Code Response."""
    return jsonify({"error": "Not found"}), error


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_POST', 500))
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(app_views, url_prefix="/api/v1")
    app.run(host=app_host, port=app_port, threaded=True)
