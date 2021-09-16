#!/usr/bin/python3
"""returns the status of the API"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """returns the status of the API"""
    return jsonify(api_status='OK')
