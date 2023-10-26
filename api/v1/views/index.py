#!/usr/bin/python3
"""Module contains route status"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Displays status of our api"""
    return jsonify({"status": "OK"})
