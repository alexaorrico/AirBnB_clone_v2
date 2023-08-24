#!/usr/bin/python3
"""Flask application that retrieves information"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns the app status"""
    return jsonify({"status": "OK"})
