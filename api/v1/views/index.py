#!/usr/bin/python3
"""Minimal Flask API Script"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Get API status."""
    return jsonify({"status": "OK"})
