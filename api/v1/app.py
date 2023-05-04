#!/usr/bin/python3
"""This module creates an instance of Flask to start our web application"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_storage(exception):
    """
    This function calls storage.close() when the request context is destroyed.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
