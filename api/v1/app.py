#!/usr/bin/python3
"""
Module: Task 4. Status of your API
returns the status of your API
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# app.url_map.strict_slashes = False
port = getenv("HBNB_API_PORT")
host = getenv("HBNB_API_HOST")

app.register_blueprint(app_views)


@app.teardown_appcontext
def call_storage_close(exception:None):
    """
    Close the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def errot_notfound(message):
    """
    Handles 404 status code
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(port= port,
            host=host,
            threaded=True)
