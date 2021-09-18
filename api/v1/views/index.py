#!/usr/bin/python3
"""Create a Index
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns status in jason format"""
    return jsonify({'status': 'OK'})
