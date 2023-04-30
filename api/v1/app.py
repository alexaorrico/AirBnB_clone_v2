#!/usr/bin/python3

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# global strict slashes
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/")

@app.teardown_appcontext
def close_storage(self):
    """
    call storage.close() at end of request
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBMB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port. threaded=True)
