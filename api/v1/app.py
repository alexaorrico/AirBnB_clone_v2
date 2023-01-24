#!/usr/bin/python3
"""Module for the api application"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def close_app(exception):
    """Close app connections"""
    storage.close()

@app.errorhandler(404)
def not_found(error_msg):
    """Handle 404"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    if host == None:
        host = "0.0.0.0"
    port = getenv("HBNB_API_PORT")
    if port is None:
        port = "5000"
    app.run(host, port, threaded=True)