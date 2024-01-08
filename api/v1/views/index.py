#!/usr/bin/python3
"""This file returns the JSON status ok"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_api():
    """home screen of the app"""
    return jsonify({"status": "OK"})
