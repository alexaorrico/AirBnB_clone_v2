#!/usr/bin/python3
"""Route to index page"""
from json import dumps
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of API"""
    return dumps({"status": "OK"})
