#!/usr/bin/python3
"""API main routes"""

import json

from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns the status in JSON format"""
    return json.dumps({"status": "OK"})
