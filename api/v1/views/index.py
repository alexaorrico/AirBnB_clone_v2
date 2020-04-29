#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
"""
Status of your API
"""

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Status of your API
    """
    return jsonify({"status":"OK"})
