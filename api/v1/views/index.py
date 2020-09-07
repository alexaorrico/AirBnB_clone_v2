#!/usr/bin/python3
"""Task 0"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('api/v1/status', strict_slashes=False)
def Index():
    """Function index"""
    return jsonify({"status": "OK"})
