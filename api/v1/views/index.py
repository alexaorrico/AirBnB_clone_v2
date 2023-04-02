#!/usr/bin/python3
"""api/v1/views/index.py"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON status"""
    return jsonify({"status": "OK"})
