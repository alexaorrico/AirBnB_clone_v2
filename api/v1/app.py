#!/usr/bin/python3
"""create a variable app, instance of Flask"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage resource at the end."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handles 404 error by returning a JSON."""
    error_dict = {"error": "Not found"}
    status_code = 404
    return (jsonify(error_dict), status_code)


if __name__ == "__main__":
    """port and host"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
