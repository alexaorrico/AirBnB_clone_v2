#!/usr/bin/python3
"""module for REST API entry point"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.errorhandler(404)
def resource_not_found(self):
    """handle 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_connection(self):
    """close DB connections"""
    storage.close()


app.register_blueprint(app_views)


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", default="0.0.0.0")
    api_port = getenv("HBNB_API_PORT", 5000)
    app.run(host=api_host, port=api_port, threaded=True)
