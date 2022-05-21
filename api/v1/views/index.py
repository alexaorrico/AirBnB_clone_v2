#!/usr/bin/python3
"""
This module defines a status route
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def index():
    """
    return staus in JSON format
    """
    return jsonify(status='OK')
