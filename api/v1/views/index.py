#!/usr/bin/python3
""" a route /status on the object app_views that returns 
    a JSON: "status": Ok
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """routes the url status"""
    return jsonify({"status": "OK"})

