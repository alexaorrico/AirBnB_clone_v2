#!/usr/bin/python3
"""Index view for api v1"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})
