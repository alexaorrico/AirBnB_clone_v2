#!/usr/binpython3
"""
app setup for Airbnb_Clone_v3
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)

app.url_map.strict.strict_slashes = False

@app.errorhandler
def page_not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def close(exception):
    storage.close
if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPort = getenv("HBNB_API_PORT", default=5000)
    app.run(host=apiHost, port=int(apiPort), threaded=True)