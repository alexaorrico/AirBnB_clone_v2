#!/usr/bin/python3
"""Index route"""
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """returns the status of the api"""
    return jsonify({"status": "OK"})