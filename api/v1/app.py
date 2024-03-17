#!/usr/bin/python3
""" Starts instance of Flask application for communication with API """
from flask import Flask, jsonify
from flask_cors import CORS
import os
from models import storage
from api.v1.views import app_views


# Set up instance of Flask
app = Flask(__name__)


# Register app_view blueprint
app.register_blueprint(app_views)

# Testing to see if enabling CORS will
# correct connection issues.
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Error Handling for 404 status.
# Using JSON...
@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors, which returns a JSON
    formatted response. """
    return jsonify({"error": "Not found"}), 404


# Teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()


if __name__ == "__main__":
    # Get environment variables and set defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run Flask app, with debug and threaded options
    app.run(host=host, port=port, debug=True, threaded=True)
