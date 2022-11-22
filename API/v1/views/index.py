#!/usr/bin/python3
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """check status"""
    return jason.dumps("status": "OK")