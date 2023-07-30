#!/usr/bin/python3
"""Index view module"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """get the status of the API"""
    return jsonify(status='OK')