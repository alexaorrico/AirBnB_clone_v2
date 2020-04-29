#!/usr/bin/python3
"""
Status of your API
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Status of your API
    """
    return jsonify({"status":"OK"})
