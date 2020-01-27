#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def status():
    """status ok"""
    return jsonify({"status": "0K"})
