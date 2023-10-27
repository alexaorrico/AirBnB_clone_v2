#!/usr/bin/python3
""" index module """

from api.v1.views import app_views

@app_views.route('/status')
def status_json():
    """returns the status"""
    return {"status": "OK"}
