#!/usr/bin/python3
"""Index for API routes v1"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a json for the state of the API"""
    return jsonify({'status': 'OK'})
