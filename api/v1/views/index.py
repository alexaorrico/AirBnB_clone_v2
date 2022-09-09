#!/usr/bin/python3
"""It's time to start your API. Your first endpoint\
(route) will be to return the status of your API"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status()
    """returns status OK if app is working"""
    return jsonify({"status": "OK"})
