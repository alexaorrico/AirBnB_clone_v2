#!/usr/bin/python3
"""module"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON with status: OK"""
    return jsonify({"status": "OK"})
