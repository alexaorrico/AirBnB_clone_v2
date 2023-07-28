#!/usr/bin/python3
"""The Developnment of a REST API"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(exc):
    """when the app is close"""
    storage.close()


@app.errorhandler(404)
def error_handler(e):
    """Return 404"""
    data = {"error": "Not found"}
    return jsonify(data), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
