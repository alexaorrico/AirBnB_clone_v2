#!/usr/bin/python3
"""
    index file for v1 api
"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Return a JSON of the status"""
    return {"status": "OK"}
