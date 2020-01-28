#!/usr/bin/python3
"""
Index module
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """return dictionary with status"""
    return {"status": "OK"}
