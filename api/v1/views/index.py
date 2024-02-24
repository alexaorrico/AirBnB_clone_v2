#!/usr/bin/python3
"""
    import app_views from api.v1.views
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON response for the status"""
    return jsonify({"status": "OK"})
