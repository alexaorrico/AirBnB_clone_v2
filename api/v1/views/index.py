#!/usr/bin/python3

"""
This module contains some utility functions for the API
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """
    Returns Status OK code.
    """
    return jsonify({"status": "OK"})


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """
    Returns 200: Status Okay
    """
    return jsonify({"status": "OK"})
