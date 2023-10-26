#!/usr/bin/python3
"""documented module"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """retuens the status"""
    return jsonify({"status": "OK"})
