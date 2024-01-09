#!/usr/bin/python3
"""
This module defines routes related to the status of the API
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return JSON status response
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count():
    """
    Return JSON stats response
    """
    return jsonify({"states": storage.count("State")})
