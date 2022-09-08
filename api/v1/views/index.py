#!/usr/bin/python3
"""
Index instance 
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def status():
    """
    Returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})
    