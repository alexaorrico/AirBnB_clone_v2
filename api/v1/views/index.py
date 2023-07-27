#!/usr/bin/python3
"""
Module that contains API endpoints
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Function that returns status in json format"""
    return jsonify({"status": "OK"})
