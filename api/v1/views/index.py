#!/usr/bin/python3
"""
Creates a route for app_views
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """represents the route /status"""
    return {"status": "OK"}
