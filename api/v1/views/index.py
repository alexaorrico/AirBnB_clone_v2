#!/usr/bin/python3
""" Index Module"""

from api.v1.views import app_views

@app.route('/status')
def status():
    return({"status": "OK"})

