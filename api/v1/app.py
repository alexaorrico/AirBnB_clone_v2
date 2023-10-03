#!/usr/bin/python3
"""
Flask application, initialize a Flask app and register blueprints
"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

# Register the app_views blueprint for API routes
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for API routes
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Closes the running SQLAlchemy session when the app context ends.
    Args:
        exception (Exception): Any exception that occurred during app context.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handles 404 (Not Found) errors by returning a JSON response.
    Args:
        error (Exception): The exception associated with the 404 error.
    Returns:
        Response: A JSON response with a 404 status code and an error message.
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Get the host and port from environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    
    # Run the Flask app with the specified host, port, and in threaded mode
    app.run(host=host, port=port, threaded=True)
