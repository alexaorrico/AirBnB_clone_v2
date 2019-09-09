#!/usr/bin/python3
"""Module for app_views /status route"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=["GET"])
def status():
    """Return /status api route"""
    return jsonify({"status": "OK"})
