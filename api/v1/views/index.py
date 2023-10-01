#!/usr/bin/python3
"""api status"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Return the status of your API"""
    return jsonify({"status": "OK"})
