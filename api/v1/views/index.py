#!/usr/bin/python3
"""
Contains the app module
"""
from v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns a JSON response"""
    return jsonify({"status": "OK"})
