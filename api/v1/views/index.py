#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_():
    """Initial status
    """
    stats = {"status": "OK"}
    return jsonify(stats)

@app_views.route('/api/v1/stats',)
def count_():
    """Count all
    """
    return jsonify
