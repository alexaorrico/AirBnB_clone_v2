#!/usr/bin/python3
"""
Module contains status endpoint
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """
    Endpoint to get API status
    """
    return jsonify({"status": "OK"})
