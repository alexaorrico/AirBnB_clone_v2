#!/usr/bin/python3
"""Index page"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def hbnbStatus():
    """Returns status of the server"""
    return jsonify({"status": "OK"})
