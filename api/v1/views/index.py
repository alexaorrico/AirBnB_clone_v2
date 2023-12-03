#!/usr/bin/python3
"""This module creates a route that returns a JSON"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """This function returns a JSON string"""
    return jsonify({"status": "OK"})
