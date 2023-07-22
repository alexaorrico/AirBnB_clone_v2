#!/usr/bin/python3
"""App Index"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Get status of API"""
    return jsonify({"status": "OK"})
