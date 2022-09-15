#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_():
    """Initial status
    """
    stats = {"status": "OK"}
    return jsonify(stats)
