#!/usr/bin/python3
"""
    Create a route
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    return status ok json
    """
    return jsonify({"status": "OK"})
