#!/usr/bin/python3
"""
views blueprint routes
"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route("/status")
def api_status():
    return jsonify(status="OK")
