#!/usr/bin/python3
""" index.py to connect with API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return status of the app"""
    return jsonify({"status": "OK"})
