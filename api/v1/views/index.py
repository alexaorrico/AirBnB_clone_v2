#!/usr/bin/python3

"""
Route that returns status
"""

from api.v1.views.index import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    """return status"""
    return {"status": "OK"}
