#!/usr/bin/python3
"""_summary_"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def api_status():
    """_summary_"""
    response = {"status": "OK"}
    return jsonify(response)
