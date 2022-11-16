#!/usr/bin/python3
"""
initialization of app
"""

from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv

# Flask app
app = Flask(__name__)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# Cross-Origin Resourse Sharing
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def shutdown(exception):
    """
    closes storage
    """
    storage.close()


@app.errorhandler(Exception)
def not_found(error):
    """Return error in JSON and status"""
    return make_response(jsonify({"error": "Not Found"}), 404)


if __name__ == "__main__":
    """
    flask app
    """
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
