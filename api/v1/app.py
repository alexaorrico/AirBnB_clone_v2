#!/usr/bin/python3
"""
Flask server (variable app)
"""

from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

# Create a CORS instance and configure it
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown app context
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors by returning a JSON response
    """
    return jsonify({"error": "Not found"}), 404

# Register the blueprint
app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", 5000), threaded=True)
