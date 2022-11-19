#!/usr/bin/python3
"""Contains routes of app_view blueprints"""

from api.v1.views import app_view
from flask import jsonify


@app_view.route("/status")
def status():
    """Returns the status of the app"""
    return jsonify({"status": "OK"})
