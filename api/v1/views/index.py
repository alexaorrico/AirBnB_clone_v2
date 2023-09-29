#!/usr/bin/python3
"""
Module for API status view.
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Retrieves the status of the API.
    ---
    responses:
    status: 200
    """
    return jsonify({"status": "OK"})
