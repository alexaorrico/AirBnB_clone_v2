#!/usr/bin/python3
"""Creationg route for Blueprint
"""
from api.v1.views import app_views


@app_views.route('/status')
def response():
    """ get status ok
    """
    dic = {"status": "OK"}
    return dic