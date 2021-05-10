#!/usr/bin/python3
""" index page"""
from api.v1.views import app_views


@app_views.route('/status')
def show():
    """ show status"""
    return {"status": "OK"}
