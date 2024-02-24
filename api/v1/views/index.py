#!/usr/bin/python3
"""define routes of blueprint"""

from api.v1.views import app_views
from models import storage

@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK",
    }
