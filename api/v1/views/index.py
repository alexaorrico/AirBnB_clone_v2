#!/usr/bin/python3
"""api index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """blueprints route"""
    return jsonify({"status": "OK"})
