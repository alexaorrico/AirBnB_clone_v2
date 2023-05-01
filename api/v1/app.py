#!/usr/bin/python3
"""Flask web Api"""
import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
""" flask web app instance"""
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown_storage(exception):
    """Closes the database connection at the end of the request."""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """handles a 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True)
