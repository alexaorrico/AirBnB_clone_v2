#!/usr/bin/python3
import os
from flask import Flask, jsonify, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# Create a Flask instance
app = Flask(__name__)

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)

# Cross-Origin Resource Sharing
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors by returning a JSON response."""
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == "__main__":
    # Run the Flask server
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
