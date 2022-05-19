#!/usr/bin/python3
"""
index module witch define an index page
"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns a JSON: 'status': 'OK'"""
    return {"status": "OK"}
