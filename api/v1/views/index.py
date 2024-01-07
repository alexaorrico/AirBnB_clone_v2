#!/usr/bin/python3
"""
    Default index api index
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """
        Returns JSON Format
    """
    return jsonify(status="OK")
