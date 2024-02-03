#!/usr/bin/python3
"""
Create routes for index
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status OK"""
    return jsonify(status="OK")
