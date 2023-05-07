#!/usr/bin/python3
"""API index module"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a status page response
    """
    return jsonify({"status": "OK"})
