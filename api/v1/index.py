#!/usr/bin/python3
"""Index for the API"""
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def ret_status():
    """funct that returns status ok"""
    return jsonify({"status": "OK"})
