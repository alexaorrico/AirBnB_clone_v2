#!/usr/bin/python3
"""Index module"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def check_status():
    """Returns status of the flask app"""
    return jsonify({"status": "OK"})
