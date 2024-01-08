#!/usr/bin/python3
"""
Status of your API
setting up a Flask API with specific endpoints
"""

from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="0.0.0.0")

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors."""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
            threaded=True, debug=True)
