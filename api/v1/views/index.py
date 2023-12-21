#!/usr/bin/python3
"""Index"""
from flask import jsonify
from api.v1.views import app_views

from models import storage

@app_views.route("/status", strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})