#!/usr/bin/python3
"""Index view for api v1"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})
