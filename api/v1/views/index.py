#!/usr/bin/python3
"""index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_status():
    """returns a JSON string of the status in a 200 response"""
    return jsonify({"status": "OK"})
