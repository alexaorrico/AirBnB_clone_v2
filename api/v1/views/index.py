#!/usr/bin/python3
"""
View routes
"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    d = {"status": "OK"}
    return d
