#!/usr/bin/python3

"""Bootstap for view"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """get status ok"""
    return {"status": "OK"}
