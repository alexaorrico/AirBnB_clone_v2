#!/usr/bin/python3
"""
    This is the index page handler for Flask.
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
        Flask route at /status.
        Displays the status of the API.
    """
    return {"status": "OK"}
