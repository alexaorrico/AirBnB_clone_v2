#!/usr/bin/python3
"""create a variable app, instance of Flask"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
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
    return jsonify(error_dict), status_code


if __name__ == "__main__":
    """port and host"""
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host="localhost", port=port, threaded=True)
