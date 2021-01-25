#!/usr/bin/python3
"""Index module"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def status():
    """Returns status OK"""
    return jsonify({"status": "OK"})
