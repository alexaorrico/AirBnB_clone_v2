#!/usr/bin/python3
"""

This module defines the '/status' route that returns a JSON response.

"""

from flask import jsonify
from api.v1.views import app_views
import os


@app_views.route('/status', methods=['GET'])
def get_status():
    """Endpoint that returns a JSON response indicating the status."""
    return jsonify({"status": "OK"})
