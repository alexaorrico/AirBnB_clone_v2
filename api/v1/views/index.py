#!/usr/bin/python3
"""Returns JSON status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns the status of our API"""
    return jsonify({"status": "OK"})
