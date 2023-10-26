#!/usr/bin/python3
"""
Status view for the AirBnB API.

This module defines a view for the status of the API.

Example:
    GET /api/v1/status:
    Returns a JSON response: {"status": "OK"}
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Get the status of the API.

    Returns:
        JSON response containing the status.

    Example:
        {"status": "OK"}
    """
    return jsonify({"status": "OK"})
