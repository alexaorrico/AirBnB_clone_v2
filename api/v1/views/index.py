#!/usr/bin/python3
""" Index view
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the web server."""
    return jsonify({"status": "OK"})
