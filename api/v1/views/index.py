#!/usr/bin/python3
"""This file returns the JSON status ok"""

from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def index():
    """home screen of the app"""
    return jsonify({"status": "OK"})
