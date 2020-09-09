#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status"""
    return ({"status": "OK"})
