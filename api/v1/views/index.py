#!/usr/bin/python3
"""New Funtion index"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def reoute_status():
    """first route
    Returns:
        json: json count number of instances
    """
    return jsonify({
        "status": "OK"
    }), 200
