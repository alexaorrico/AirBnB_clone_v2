#!/usr/bin/python3
"""crate python file routes the flask API"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """retrive ok status"""
    return jsonify({"status": "OK"})
