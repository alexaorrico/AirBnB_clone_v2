#!/usr/bin/python3
"""index of views"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """status of api v1"""
    return jsonify({"status": "OK"})
