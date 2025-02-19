#!/usr/bin/python3
"""
AirBnB API v1 main module
Flask application initialization, blueprint registration
and 404 error handling for JSON responses.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS  # Importing CORS for cross-origin requests
import os

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """Teardown method to close storage."""
    storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    """Return json formated 404 errors (page nt found)"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
