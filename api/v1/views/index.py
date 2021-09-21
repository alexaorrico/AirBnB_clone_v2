#!/usr/bin/python3
"""JSON OK status will return"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON status ok"""
    return jsonify({"status": "OK"})
