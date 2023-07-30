#!/usr/bin/python3
"""
script that create a route /status on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """create a Json of status"""
    return (jsonify({"status": "OK"}))
