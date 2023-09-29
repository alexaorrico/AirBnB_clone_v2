#!/usr/bin/python3
"""Proceeds to import neccessary stuffs"""


from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {"status": "OK"}
