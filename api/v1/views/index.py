#!/usr/bin/python3
"""creates status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnb status"""
    return jsonify({"status": "OK"})
