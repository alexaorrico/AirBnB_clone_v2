#!/usr/bin/python3
"""
Flask application instance
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register blueprint for app views
app.register_blueprint(app_views)

# Create a CORS instance allowing all origins
CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database again at the end of the request."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000, threaded=True)
