#!/usr/bin/python3
"""Routes Controller"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Define route"""
    return jsonify({"status": "OK"})
