#!/usr/bin/python3
"""config file"""

from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcont(self):
    """ends db session"""
    storage.close()


@app.errorhandler(404)
def not_reached(error):
    """Handle non existing pages"""
    e = {
        "error": "Not Found"
    }
    return make_response(jsonify(e), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    ports = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=ports, threaded=True)
