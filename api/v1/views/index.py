#!/usr/bin/python3
"""
import view
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def api_ok():
    return jsonify({"status": "OK"})
