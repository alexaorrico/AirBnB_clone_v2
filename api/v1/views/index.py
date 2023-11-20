#!/usr/bin/python3
"""index creates route for status"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def get_status():
    """returns status"""
    return jsonify({"status": "OK"})
