#!/usr/bin/python3
"""returns json statuses for app_views routes"""

from api.v1.views import app_views
from flask import jsonify
from models import storage



@app_views.route("/status", strict_slashes=False)
def status():
    """return status OK """
    return jsonify({"status": "OK"})
