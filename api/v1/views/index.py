#!/usr/bin/python3
"""
This module defines a status route for the API.
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"})
