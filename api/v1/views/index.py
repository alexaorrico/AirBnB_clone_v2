#!/usr/bin/python3
"""
returns json status
"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route("/status")
def get_status():
    """
    return json
    """
    return jsonify({
        "status": "OK"
    })
