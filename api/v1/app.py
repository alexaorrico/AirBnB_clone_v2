#!/usr/bin/python3
"""A Flask app that used to make communication bettween #nt apps"""

# Importing modules from system files
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Importing modules from my files
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
"""Instances of Flask web application"""
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """Closing The Storage after use."""
    storage.close()


@app.errorhandler(404)
def errorhandler_404(error):
    """Thi function handle the 404 HTTP error code."""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    """To run api app, If debug is on means our output have a good view."""
    app.run(host=app_host, port=app_port, threaded=True, debug=True)
