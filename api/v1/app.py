#!/usr/bin/python3
"""
    Flask App that integrates the  API
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import requests
from os import *


app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(excep):
    """
        close sqlAlch session
    """
    storage.close()


@app.errorhandler(404)
def invalid_route(error):
    """
        comment
    """
    return jsonify({"error": "Not found"}), (404)


if __name__ == "__main__":
    app.run(host=host, port=port)
