#!/usr/bin/python3
"""
Flask App that integrates AirBnB static HTML Template
"""
import os
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

# Set flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
app.register_blueprint(app_views)

# Create a CORS instance
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    """Close the storage session after each request."""
    storage.close()


@app.errorhandler(404)
def handle_api_error(exception):
    """Returns a JSON-formatted 404 status code response."""
    return make_response(jsonify({
        "error": "Not found"
    }), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)

