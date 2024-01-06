#!/usr/bin/python3
"""index default view"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def get_status():
    """get api status"""
    return jsonify({"status": "OK"})
